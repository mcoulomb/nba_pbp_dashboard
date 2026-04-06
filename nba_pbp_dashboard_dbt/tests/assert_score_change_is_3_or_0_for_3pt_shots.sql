SELECT *
FROM {{ ref("fct_3pt_data") }}
WHERE score_change != 0 and score_change != 3