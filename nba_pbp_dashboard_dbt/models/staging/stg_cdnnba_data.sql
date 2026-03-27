
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
        cast(jumpBallRecoverdPersonId as integer) as jumpball_recovered_player_id,
        cast(jumpBallLostPersonId as integer) as jumpball_lost_player_id,
        cast(jumpBallWonPersonId as integer) as jumpball_won_player_id,
        cast(assistPersonId as integer) as assist_player_id,
        cast(foulDrawnPersonId as integer) as foul_drawn_player_id,
        cast(stealPersonId as integer) as steal_player_id,
        cast(blockPersonId as integer) as block_player_id,
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
        cast(shotResult as string) as shot_result,
        cast(description as string) as description,
        cast(descriptor as string) as descriptor,

        --misc
        cast(x as numeric) as x_loc,
        cast(y as numeric) as y_loc,
        cast(possession as integer) as possession,
        cast(edited as timestamp) as edited,
        cast(orderNumber as integer) as order_number,
        cast(isTargetScoreLastPeriod as boolean) as is_target_score_last_period,
        cast(xLegacy as numeric) as x_legacy,
        cast(yLegacy as numeric) as y_legacy,
        cast(isFieldGoal as integer) as is_field_goal,
        cast(side as string) as side,
        cast(jumpBallRecoveredName as string) as jumpball_recovered_name,
        cast(playerName as string) as player_last_name,
        cast(jumpBallWonPlayerName as string) as jumpball_won_player_name,
        cast(jumpBallLostPlayerName as string) as jump_balllost_player_name,
        cast(shotActionNumber as numeric) as shot_action_number,
        cast(reboundTotal as integer) as rebound_total,
        cast(reboundDefensiveTotal as integer) as rebound_defensive_total,
        cast(reboundOffensiveTotal as integer) as rebound_offensive_total,
        cast(pointsTotal as integer) as points_total,
        cast(assistPlayerNameInitial as string) as assist_player_name_initial,
        cast(assistTotal as integer) as assist_total,
        cast(officialId as integer) as official_id,
        cast(foulPersonalTotal as integer) as foul_personal_total,
        cast(foulTechnicalTotal as integer) as foul_technical_total,
        cast(foulDrawnPlayerName as string) as foul_drawn_player_name,
        cast(turnoverTotal as integer) as turnover_total,
        cast(stealPlayerName as string) as steal_player_name,
        cast(blockPlayerName as string) as block_player_name

    from source_data
)       

select * from renamed


