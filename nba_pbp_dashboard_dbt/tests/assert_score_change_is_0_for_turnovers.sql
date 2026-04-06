SELECT *
FROM {{ ref("fct_turnover_data") }}
WHERE score_change != 0