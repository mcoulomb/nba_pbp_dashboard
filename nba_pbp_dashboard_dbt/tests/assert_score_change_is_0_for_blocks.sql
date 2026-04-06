SELECT *
FROM {{ ref("fct_blocks_data") }}
WHERE score_change != 0