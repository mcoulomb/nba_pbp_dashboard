SELECT *
FROM {{ ref("fct_records_by_year") }}
WHERE wins + losses != 72 
AND year = {{ var('covid_year') }}