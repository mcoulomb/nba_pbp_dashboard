
/*
    Staging table to materialize external pbp table.
*/

{{ config(
    materialized='table',
    cluster_by = ["team_id", "player_id", "period", "action_type"]
    )
}}

with int_cdnnba_data as (
    select * from {{ ref('stg_cdnnba_data') }}
)

select * from int_cdnnba_data


