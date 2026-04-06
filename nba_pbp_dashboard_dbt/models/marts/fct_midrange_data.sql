/*
    Fact table for 3 point shooting.
*/

{{ config(
    materialized='table',
    )
}}

with fct_midrange as (
    select
        game_id,
        player_id,
        player_name,
        action_number,
        order_number,
        team_tricode,
        home_team,
        away_team,
        team_in_lead,
        prev_team_in_lead,
        lead_change,
        is_garbage_time,
        period,
        minutes_remaining,
        seconds_remaining,
        home_score,
        home_score_diff,
        away_score,
        away_score_diff,
        score_diff,
        score_change,
        action_type,
        action_sub_type,
        area,
        area_detail,
        shot_distance,
        shot_result,
        x_location,
        y_location,
        action_qualifiers
    from {{ ref("int_pbp_data") }} as pbp_data
    where
        is_field_goal = true
        and action_type = '2pt'
        and action_sub_type IN ('jump shot', 'shot', 'hook')
)

select * from fct_midrange