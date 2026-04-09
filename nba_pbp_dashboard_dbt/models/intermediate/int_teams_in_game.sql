{{ config(
    materialized='table'
    )
}}

with int_data as (
    select * from {{ ref('int_cdnnba_data') }}
),

int_teams_in_game as (
SELECT *
FROM(
SELECT 
  game_id, 
  team_tricode, 
  LEAD(team_tricode) OVER (partition by game_id ORDER BY game_id) as team_tricode2
  from
  (
select distinct team_tricode, game_id
FROM int_data
where team_tricode IS NOT NULL group by team_tricode, game_id order by game_id
  )
)
where team_tricode2 IS NOT NULL
 order by game_id
)

select * from int_teams_in_game