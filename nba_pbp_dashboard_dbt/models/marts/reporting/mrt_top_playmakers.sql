SELECT 
    assist_data.*,
    player_data.player_name 
FROM (
    SELECT assist_player_id, 
        CASE 
            WHEN action_type = '3pt' Then '3pt'
            ELSE 'Dunk'
        END as play_result,
        period,
        count(*) as play_quantity
    FROM {{ ref('int_cdnnba_data') }}
    WHERE 
        is_field_goal = true
        AND period_type='REGULAR'
        AND (action_type='3pt' OR action_sub_type='DUNK')
        AND shot_result = 'Made' 
        AND assist_player_id IS NOT NULL 
    GROUP BY period, play_result, assist_player_id ) as assist_data
LEFT OUTER JOIN {{ ref('dim_player_data') }} as player_data 
ON assist_data.assist_player_id = player_data.player_id 
ORDER BY play_quantity DESC