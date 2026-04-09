{{ config(
    materialized='table',
    )
}}

SELECT 
    year, 
    team_tricode, 
    action_type, 
    count(*) as shot_count
FROM {{ ref('int_pbp_data') }} 
    where is_field_goal = true 
GROUP BY team_tricode, year, action_type 
ORDER BY YEAR, team_tricode