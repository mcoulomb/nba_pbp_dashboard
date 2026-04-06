SELECT *
FROM {{ ref("fct_midrange_data") }}
WHERE score_change != 0 and score_change != 2