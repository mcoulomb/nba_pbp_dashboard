SELECT *
FROM {{ ref("fct_steals_data") }}
WHERE score_change != 0