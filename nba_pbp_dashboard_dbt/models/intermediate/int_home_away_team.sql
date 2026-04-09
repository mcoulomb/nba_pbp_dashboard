{{ config(
    materialized='table'
)
}}

with int_data as (
    select * from {{ ref('int_cdnnba_data') }}
),

int_home_away_determine_first_team as (
select home_away_array[offset(0)] as temp_struct,game_id, year from (
SELECT array_agg(struct(home_team_temp, away_team_temp, order_number)) as home_away_array, game_id, year from (
select    
                CASE
                    WHEN score_diff = home_score_diff THEN team_tricode
                    ELSE null
                END as home_team_temp,  
                CASE
                    WHEN score_diff = away_score_diff THEN team_tricode
                    ELSE null
                END as away_team_temp,
            game_id,
            year,
            order_number
    from int_data
     where shot_result = 'made' and home_score_diff != away_score_diff order by game_id, order_number
) GROUP BY game_id, year
)
),

int_home_away_fill_in_missing_team as (
SELECT CASE 
		WHEN temp_struct.home_team_temp IS NULL
			AND temp_struct.away_team_temp != team_tricode
			THEN team_tricode
		WHEN temp_struct.home_team_temp IS NULL
			AND temp_struct.away_team_temp != team_tricode2
			THEN team_tricode2
		WHEN temp_struct.home_team_temp = team_tricode
			THEN team_tricode
		WHEN temp_struct.home_team_temp = team_tricode2
			THEN team_tricode2
		END AS home_team
	,CASE 
		WHEN temp_struct.away_team_temp IS NULL
			AND temp_struct.home_team_temp != team_tricode
			THEN team_tricode
		WHEN temp_struct.away_team_temp IS NULL
			AND temp_struct.home_team_temp != team_tricode2
			THEN team_tricode2
		WHEN temp_struct.away_team_temp = team_tricode
			THEN team_tricode
		WHEN temp_struct.away_team_temp = team_tricode2
			THEN team_tricode2
		END AS away_team
	,home_away_first_pass.game_id
    ,home_away_first_pass.year
	
FROM int_home_away_determine_first_team home_away_first_pass
JOIN (
	SELECT *
	FROM {{ ref("int_teams_in_game") }}
	WHERE team_tricode IS NOT NULL
		AND team_tricode2 IS NOT NULL
	ORDER BY game_id
	) AS teams_in_game ON teams_in_game.game_id = home_away_first_pass.game_id
ORDER BY game_id
)

select * from int_home_away_fill_in_missing_team