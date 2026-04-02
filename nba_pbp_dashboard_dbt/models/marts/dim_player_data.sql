
/*
    Dimension table for players. The MAX aggregation is used on the player_name field to ensure that we get a single name for each player_id and team_tricode combination.
*/

{{ config(
    materialized='table',
    )
}}

with int_player_data as (
    select distinct
        player_id,
        MAX(player_name) as player_name,
        team_tricode
     from {{ ref('int_cdnnba_data') }}
     where player_id != 0 and player_name is not null
     GROUP BY player_id, team_tricode
)

select * from int_player_data


