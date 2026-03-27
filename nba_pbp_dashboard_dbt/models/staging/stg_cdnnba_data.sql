
/*
    Staging table to materialize external pbp table.
*/

{{ config(
    materialized='view',
    )
}}

with source_data as (
    select * from {{ source('raw', 'nba_pbp_data_external') }}
),

renamed as (
    select
        -- identifiers
        cast(gameId as integer) as game_id,
        cast(actionNumber as integer) as action_number,
        cast(personId as integer) as player_id,
        cast(teamId as integer) as team_id,
        cast(teamTricode as string) as team_tricode,
        cast(playerNameI as string) as player_name,
        cast(jumpBallRecoverdPersonId as integer) as jump_ball_recovered_player_id,
        cast(jumpBallLostPersonId as integer) as jump_ball_lost_player_id,
        cast(assistPersonId as integer) as assist_player_id,
        cast(foulDrawnPersonId as integer) as foul_drawn_player_id,
        cast(stealPersonId as integer) as block_player_id,
        cast(personIdsFilter as string) as players_id_filter,

        -- clock/period/score
        cast(period as integer) as period,
        cast(periodType as string) as periodType,
        cast(clock as string) as clock,
        cast(timeActual as timestamp) as actual_time,
        cast(scoreHome as integer) as home_score,
        cast(scoreAway as integer) as away_score,


        -- actions
        cast(actionType as string) as action_type,
        cast(subType as string) as action_sub_type,
        cast(qualifiers as string) as action_qualifiers,
        cast(area as string) as area,
        cast(areaDetail as string) as area_detail,
        cast(shotDistance as numeric) as shot_distance,
        cast(shotResult as string) as shot_result
    from source_data
)       

select * from renamed


