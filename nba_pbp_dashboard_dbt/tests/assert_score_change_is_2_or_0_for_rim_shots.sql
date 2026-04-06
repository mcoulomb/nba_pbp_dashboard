SELECT *
FROM {{ ref("fct_rim_shooting_data") }}
WHERE score_change != 0 and score_change != 2