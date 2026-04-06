SELECT *
FROM {{ ref("fct_records_by_year") }}
WHERE wins + losses != 82
AND year != '{{ var('covid_year') }}' AND year != '{{ var('current_year') }}'