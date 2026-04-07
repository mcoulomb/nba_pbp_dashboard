/*
    Intermediate play by play data table. This model is mainly responsible for adding home and away team information and tracking lead changes.
*/

{{ config(
    materialized='table',
    cluster_by = ["year", "is_field_goal"]
    )
}}

with int_cdnnba_data as (
    select * from {{ ref('int_cdnnba_data') }}
),

int_pbp_data1 as (
    select 
    -- identifiers
        pbp_data.game_id,
        pbp_data.year,
        game_type,
        action_number,
        player_id,
        team_id,
        team_tricode,
        player_name,
        jumpball_recovered_player_id,
        jumpball_lost_player_id,
        jumpball_won_player_id,
        assist_player_id,
        foul_drawn_player_id,
        steal_player_id,
        block_player_id,
        players_id_filter,
        order_number,

        -- clock/period/score
        period,
        period_type,
        clock,
        minutes_remaining,
        seconds_remaining,
        home_score,
        away_score,
        home_score_diff,
        away_score_diff,
        score_diff,
        score_change,
        is_garbage_time,


        -- actions
        action_type,
        action_sub_type,
        action_qualifiers,
        area,
        area_detail,
        shot_distance,
        shot_result,
        case
            when x_location > 50 then (x_location * -1) + 100
            else x_location
        end as x_location_converted,
        y_location / 2 as y_location_converted,
        description,
        descriptor,
        is_field_goal,
        home_away_data.home_team,
        home_away_data.away_team,
    case
        when home_score_diff > 0 then home_away_data.home_team
        when away_score_diff > 0 then home_away_data.away_team
        else null
    end as team_in_lead_processing
    from int_cdnnba_data as pbp_data join {{ ref("int_home_away_team" )}} as home_away_data on pbp_data.game_id = home_away_data.game_id
    order by pbp_data.game_id, order_number
),

-- When determining a lead change, a team is considered in the lead until the lead fully switches to the other team. This means in the instance of a tie game the team "in the lead" was the team 
-- leading prior to the tie occuring. Because of this definition we need to look back at prior rows and track who was in the lead.
int_prev_team_lead as (
   select
   *,
   LAST_VALUE(team_in_lead_processing ignore nulls) over (partition by int_pbp_data1.game_id order by order_number asc rows between unbounded preceding AND 1 preceding) as prev_team_in_lead
   from int_pbp_data1
),

-- If the team_in_lead_processing field is null then that means the score is tied. In this case the team_in_lead should be set to the previous team_in_lead since a lead change has not yet occurred. 
int_finalize_team_lead as (
    select *,
    case
        when team_in_lead_processing is null then prev_team_in_lead
        else team_in_lead_processing
    end as team_in_lead
    from int_prev_team_lead
),

-- If the team_in_lead field does not match the prev_team_in_lead field then we know a lead change has occurred.
int_lead_change as (
   select *,
   case
    when team_in_lead != prev_team_in_lead then true
    else false
   end as is_lead_change
   from int_finalize_team_lead
)

select * from int_lead_change