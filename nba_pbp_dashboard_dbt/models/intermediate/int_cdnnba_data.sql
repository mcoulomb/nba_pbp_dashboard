
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
        actual_time,
        home_score,
        away_score,

        -- actions
        action_type,
        action_sub_type,
        action_qualifiers,
        area,
        area_detail,
        shot_distance,
        shot_result,
        description,
        descriptor,
        is_field_goal

    from {{ ref('stg_cdnnba_data') }}
)

select * from int_cdnnba_data


