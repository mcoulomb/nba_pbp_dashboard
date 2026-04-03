-- We should never have a game that has a null value in either the home_team or away_team column.
SELECT * FROM {{ ref("int_home_away_team") }} where home_team IS NULL OR away_team IS NULL