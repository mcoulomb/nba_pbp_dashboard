
/*
    Staging table to materialize external pbp table.
*/

{{ config(
    materialized='table',
    )
}}

with int_player_data as (
    select distinct
        player_id,
        player_name,
        team_tricode
     from {{ ref('int_cdnnba_data') }}
     where player_id != 0 and player_name is not null
)

select * from int_player_data


