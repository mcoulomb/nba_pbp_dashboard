{{ config(
    materialized='table'
    )
}}


with fct_records_by_year as (
SELECT win_record.team
	,win_record.year
	,wins
	,losses
FROM (
	SELECT winning_team AS team
		,year
		,count(*) AS wins
	FROM {{ ref("fct_final_score") }}
	GROUP BY year
		,winning_team
	ORDER BY year
	) AS win_record
JOIN (
	SELECT losing_team AS team
		,year
		,count(*) AS losses
	FROM {{ ref("fct_final_score") }}
	GROUP BY year
		,losing_team
	ORDER BY year
	) AS loss_record ON win_record.team = loss_record.team
	AND win_record.year = loss_record.year
)

select * from fct_records_by_year