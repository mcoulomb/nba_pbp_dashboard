{{ config(
    materialized='table',
    partition_by= {
        "field":"year",
        "data_type":"integer"
    }
    )
}}

SELECT * FROM (
SELECT * FROM {{ ref("fct_3pt_data") }}
UNION ALL
SELECT * FROM {{ ref("fct_midrange_data") }}
UNION ALL
SELECT * FROM {{ ref("fct_rim_shooting_data") }}
) 