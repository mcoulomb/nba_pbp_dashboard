{{ config(
    materialized='view',
    cluster_by = []
    )
}}

with int_data as (
    select * from {{ ref('int_cdnnba_data') }}
),

int_final_score as (
SELECT 
    game_id,
    home_score,
    away_score,
    year
FROM int_data
WHERE action_type = 'game'
ORDER BY game_id
)

select * from int_final_score