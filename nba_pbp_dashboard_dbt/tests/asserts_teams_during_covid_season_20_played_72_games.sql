-- Due to the COVID shutdown in the 2019-2020 season, only 72 regular season games were played.
SELECT * FROM (
SELECT SUM(games_played) as games_played, year, team FROM (
SELECT COUNT(*) as games_played,home_team as team, year FROM `nba-pbp-dashboard.nba_pbp_dashboard_raw.int_home_away_team` GROUP BY year, home_team
UNION ALL
SELECT COUNT(*) as games_played,away_team as team, year FROM `nba-pbp-dashboard.nba_pbp_dashboard_raw.int_home_away_team` GROUP BY year, away_team
)
GROUP BY year, team
ORDER BY year, team
)
WHERE games_played != 72
AND year = '{{ var('covid_year') }}'