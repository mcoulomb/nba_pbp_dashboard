{{ config(
    materialized='table'
    )
}}


with fct_final_score as (
select 
    game_result.game_id,
    game_result.home_score,
    game_result.away_score,
    home_away.home_team,
    home_away.away_team,
    game_result.year,
    case
        when game_result.home_score > game_result.away_score then home_away.home_team
        else home_away.away_team
    end as winning_team,
        case
        when game_result.home_score < game_result.away_score then home_away.home_team
        else home_away.away_team
    end as losing_team,
FROM {{ ref("int_game_result") }} as game_result join {{ ref("int_home_away_team") }} as home_away on game_result.game_id = home_away.game_id
)

select * from fct_final_score