
/*
    Staging table to materialize external pbp table.
*/

{{ config(
    materialized='table',
    cluster_by = ["year", "is_field_goal"]
    )
}}

with int_cdnnba_data as (
        select
        -- identifiers
        game_id,
        substr(game_id,2,2) as year,
        CASE
            WHEN (substr(game_id,1,1) = '2') THEN 'R'
            ELSE 'P'
        END as game_type,
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

        -- clock/period/score
        period,
        periodType,
        clock,
        CAST(substr(clock, 3, 2) as integer) as minutes_remaining,
        CAST(substr(clock, 6, 5) as numeric) as seconds_remaining,
        home_score,
        away_score,
        home_score - away_score as home_score_diff,
        away_score - home_score as away_score_diff,
        abs(home_score - away_score) as score_diff,
        CASE
            WHEN shot_result = 'made' and action_type = 'freethrow' THEN 1
            WHEN shot_result = 'made' and action_type = '2pt' THEN 2
            WHEN shot_result = 'made' and action_type = '3pt' THEN 3
        END as score_change,


        -- actions
        action_type,
        action_sub_type,
        action_qualifiers,
        area,
        area_detail,
        shot_distance,
        shot_result,
        x_location,
        y_location,
        description,
        descriptor,
        is_field_goal

    from {{ ref('stg_cdnnba_data') }}
),



int_garbage_time_sweep_1_data as (
    select 
            CASE
                WHEN (score_diff >= 25 AND period >= 4 AND minutes_remaining BETWEEN 9 and 12 AND seconds_remaining BETWEEN 0 AND 59.99) THEN true
                WHEN (score_diff >= 20 AND period >= 4 AND minutes_remaining BETWEEN 6 and 9 AND seconds_remaining BETWEEN 0 AND 59.99) THEN true
                WHEN (score_diff >= 15 AND period >= 4 AND minutes_remaining BETWEEN 1 and 6 AND seconds_remaining BETWEEN 0 AND 59.99) THEN true
                WHEN (score_diff >= 9  AND period >= 4 AND minutes_remaining = 0 AND seconds_remaining BETWEEN 0 AND 59.99) THEN true
                ELSE false
            END as is_garbage_time_sweep_1,
            *
    from int_cdnnba_data
),

int_garbage_time_sweep_2_data as (
    SELECT 
        CASE
            WHEN (SELECT count(*) FROM int_garbage_time_sweep_1_data as inner_query where inner_query.game_id = outer_query.game_id and inner_query.action_number >= outer_query.action_number and inner_query.is_garbage_time_sweep_1 = false) > 0
            THEN false
            ELSE is_garbage_time_sweep_1
        END as is_garbage_time,
        *
    FROM int_garbage_time_sweep_1_data as outer_query
)


select * from int_garbage_time_sweep_2_data


