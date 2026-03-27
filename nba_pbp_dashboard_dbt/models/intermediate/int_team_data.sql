
/*
    Staging table to materialize external pbp table.
*/

{{ config(
    materialized='table',
    )
}}

with int_team_data as (
    select distinct
        team_id,
        team_tricode
     from {{ ref('int_cdnnba_data') }}
     where team_id != 0 and team_tricode is not null
)

select * from int_team_data


