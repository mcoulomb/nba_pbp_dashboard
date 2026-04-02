
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
        cast(gameId as string) as game_id,
        cast(actionNumber as integer) as action_number,
        cast(personId as integer) as player_id,
        cast(teamId as integer) as team_id,
        cast(lower(teamTricode) as string) as team_tricode,
        cast(lower(playerNameI) as string) as player_name,
        cast(jumpBallRecoverdPersonId as integer) as jumpball_recovered_player_id,
        cast(jumpBallLostPersonId as integer) as jumpball_lost_player_id,
        cast(jumpBallWonPersonId as integer) as jumpball_won_player_id,
        cast(assistPersonId as integer) as assist_player_id,
        cast(foulDrawnPersonId as integer) as foul_drawn_player_id,
        cast(stealPersonId as integer) as steal_player_id,
        cast(blockPersonId as integer) as block_player_id,
        cast(lower(personIdsFilter) as string) as players_id_filter,

        -- clock/period/score
        cast(period as integer) as period,
        cast(lower(periodType) as string) as periodType,
        cast(lower(clock) as string) as clock,
        cast(timeActual as timestamp) as actual_time,
        cast(scoreHome as integer) as home_score,
        cast(scoreAway as integer) as away_score,

        -- actions
        cast(lower(actionType) as string) as action_type,
        cast(lower(subType) as string) as action_sub_type,
        cast(lower(qualifiers) as string) as action_qualifiers,
        cast(lower(area) as string) as area,
        cast(lower(areaDetail) as string) as area_detail,
        cast(shotDistance as numeric) as shot_distance,
        cast(lower(shotResult) as string) as shot_result,
        cast(lower(description) as string) as description,
        cast(lower(descriptor) as string) as descriptor,
        cast(isFieldGoal as boolean) as is_field_goal,

        --misc
        cast(x as numeric) as x_location,
        cast(y as numeric) as y_location,
        cast(possession as integer) as possession,
        cast(edited as timestamp) as edited,
        cast(orderNumber as integer) as order_number,
        cast(isTargetScoreLastPeriod as boolean) as is_target_score_last_period,
        cast(xLegacy as numeric) as x_legacy,
        cast(yLegacy as numeric) as y_legacy,
        cast(lower(side) as string) as side,
        cast(lower(jumpBallRecoveredName) as string) as jumpball_recovered_name,
        cast(lower(playerName) as string) as player_last_name,
        cast(lower(jumpBallWonPlayerName) as string) as jumpball_won_player_name,
        cast(lower(jumpBallLostPlayerName) as string) as jump_balllost_player_name,
        cast(shotActionNumber as numeric) as shot_action_number,
        cast(reboundTotal as integer) as rebound_total,
        cast(reboundDefensiveTotal as integer) as rebound_defensive_total,
        cast(reboundOffensiveTotal as integer) as rebound_offensive_total,
        cast(pointsTotal as integer) as points_total,
        cast(lower(assistPlayerNameInitial) as string) as assist_player_name_initial,
        cast(assistTotal as integer) as assist_total,
        cast(officialId as integer) as official_id,
        cast(foulPersonalTotal as integer) as foul_personal_total,
        cast(foulTechnicalTotal as integer) as foul_technical_total,
        cast(lower(foulDrawnPlayerName) as string) as foul_drawn_player_name,
        cast(turnoverTotal as integer) as turnover_total,
        cast(lower(stealPlayerName) as string) as steal_player_name,
        cast(lower(blockPlayerName) as string) as block_player_name

    from source_data
)       

select * from renamed


