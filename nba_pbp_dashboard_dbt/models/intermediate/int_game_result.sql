{{ config(
    materialized='table'
    )
}}

with int_data as (
    select * from {{ ref('int_cdnnba_data') }}
),

int_game_result as (
SELECT 
    game_id,
    home_score,
    away_score,
    year
FROM int_data
WHERE action_type = 'game'
ORDER BY game_id
)

select * from int_game_result