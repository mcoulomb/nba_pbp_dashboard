/*
    Fact table for turnovers.
*/

{{ config(
    materialized='table',
    )
}}

with fct_turnover_data as (
    select
        game_id,
        player_id,
        player_name,
        year,
        action_number,
        order_number,
        team_tricode,
        home_team,
        away_team,
        team_in_lead,
        prev_team_in_lead,
        is_lead_change,
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
        x_location_converted,
        y_location_converted,
        action_qualifiers
    from {{ ref("int_pbp_data") }} as pbp_data
    where
        action_type = 'turnover'
)

select * from fct_turnover_data