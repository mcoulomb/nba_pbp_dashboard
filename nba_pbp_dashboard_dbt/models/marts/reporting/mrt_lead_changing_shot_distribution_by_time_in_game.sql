WITH three_point_normal_time AS (SELECT count(*) as shot_count,'3pt' as shot_type, 'normal' as game_time, year FROM {{ ref("fct_3pt_data") }} where is_lead_change = true and is_garbage_time = false and (period < 4 or (period = 4 and minutes_remaining > 2)) group by year),
three_point_end_game as (SELECT count(*) as shot_count,'3pt' as shot_type, 'end' as game_time, year FROM {{ ref("fct_3pt_data") }} where is_lead_change = true and is_garbage_time = false and (period = 4 and minutes_remaining < 3) or (period > 4 and minutes_remaining < 5) group by year),
midrange_normal_time as (SELECT count(*) as shot_count,'midrange' as shot_type, 'normal' as game_time, year FROM {{ ref("fct_midrange_data") }} where is_lead_change = true and is_garbage_time = false and (period < 4 or (period = 4 and minutes_remaining > 2)) group by year),
midrange_end_game as (SELECT count(*) as shot_count,'midrange' as shot_type, 'end' as game_time, year FROM {{ ref("fct_midrange_data") }} where is_lead_change = true and is_garbage_time = false and (period = 4 and minutes_remaining < 3) or (period > 4 and minutes_remaining < 5) group by year),
rim_normal_time as (SELECT count(*) as shot_count, 'rim' as shot_type, 'normal' as game_time, year FROM {{ ref("fct_rim_shooting_data") }} where is_lead_change = true and is_garbage_time = false and (period < 4 or (period = 4 and minutes_remaining > 2)) group by year),
rim_end_game as (SELECT count(*) as shot_count,'rim' as shot_type, 'end' as game_time, year FROM {{ ref("fct_rim_shooting_data") }} where is_lead_change = true and is_garbage_time = false and (period = 4 and minutes_remaining < 3) or (period > 4 and minutes_remaining < 5) group by year)

SELECT * FROM three_point_normal_time
UNION ALL 
SELECT * FROM three_point_end_game
UNION ALL
SELECT * FROM midrange_normal_time
UNION ALL
SELECT * FROM midrange_end_game
UNION ALL
SELECT * FROM rim_normal_time
UNION ALL
SELECT * FROM rim_end_game