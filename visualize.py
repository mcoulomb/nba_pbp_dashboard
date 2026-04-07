import plotly.express as px
import plotly.io as pio
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd

pio.renderers.default = 'browser'

def shot_distribution_by_year(shot_distribution_df):
    fig= px.bar(shot_distribution_df, x="year", y="shot_count", color="action_type", title="Shot Distribution By Year",hover_name="team_tricode", pattern_shape="team_tricode")
    return fig

def top_playmaker_by_period(top_playmakers_df):
    fig= px.bar(top_playmakers_df, x="period", y="play_quantity", color="play_result", title="Dunk and 3s Assist Leaders by Period",facet_row="player_name")
    return fig

def time_based_shot_distribution_by_year(time_based_shot_distribution_df):
    fig = px.line(time_based_shot_distribution_df, x="year", y="shot_percentage", line_dash="game_time", color='shot_type', title="Distribution of Shot Types causing a Lead Change based on Time in Game", color_discrete_sequence=['#FF0000', 'orange', '#0000FF'])
    return fig

def shot_chart(shot_chart_df_l, shot_chart_df_t):
# Create hexbin mapbox using figure_factory
    fig, ax = plt.subplots(figsize=(12, 6))
    hexbin_l = ax.hexbin(shot_chart_df_l["y_location_converted"], shot_chart_df_l["x_location_converted"],C=shot_chart_df_l["is_shot_made"], gridsize=20, cmap="Reds")
    hexbin_t = ax.hexbin(shot_chart_df_t["y_location_converted"], shot_chart_df_t["x_location_converted"], gridsize=20,C=shot_chart_df_t["is_shot_made"], cmap="Reds", mincnt=50)
    ax.set_title('Boston Celtics 24-25 Season Shooting Chart')

    #if(len(hexbin_l.get_array()) > len(hexbin_t.get_array())):
        #pad_length = len(hexbin_l.get_array()) - len(hexbin_t.get_array())
        #hexbin_t_array = hexbin_t.get_array()
        #hexbin_t_array = np.pad(hexbin_t_array, (0, pad_length), 'constant')
        #hexbin_t.set_array(hexbin_t_array)
    
    df_league = pd.DataFrame(data=hexbin_l.get_offsets(), columns=['x','y'])
    df_league['league_shooting'] = hexbin_l.get_array().tolist()

    df_team = pd.DataFrame(data=hexbin_t.get_offsets(), columns=['x','y'])
    df_team['team_shooting'] = hexbin_t.get_array().tolist()

    df_sorted_league = df_league.sort_values(by="x")
    df_sorted_team = df_team.sort_values(by="x")

    league_array = hexbin_l.get_offsets()

    la, lb = np.hsplit(league_array, 2) 
    la = np.squeeze(la) # array([1, 3, 5])
    lb = np.squeeze(lb) # array([2, 4, 6])

    la = np.round(la,0)
    lb = np.round(lb,0)
    single_value_coordinate_l = (la*10000) + lb

    single_value_array_l = np.column_stack([single_value_coordinate_l, hexbin_l.get_array()])

    df_league = pd.DataFrame(single_value_array_l,columns=["coordinate","league_shooting_pct"])

    team_array = hexbin_t.get_offsets()

    ta, tb = np.hsplit(team_array, 2) 
    ta = np.squeeze(ta) # array([1, 3, 5])
    tb = np.squeeze(tb) # array([2, 4, 6])

    ta = np.round(ta,0)
    tb = np.round(tb,0)

    single_value_coordinate_t = (ta*10000) + tb

    single_value_array_t = np.column_stack([single_value_coordinate_t, hexbin_t.get_array()])

    df_team = pd.DataFrame(single_value_array_t,columns=["coordinate","team_shooting_pct"])

    df_team.sort_values(by="coordinate",inplace=True)
    df_league.sort_values(by="coordinate",inplace=True)

    df_merged = pd.merge_asof(df_team,df_league, on=['coordinate'],direction='nearest',tolerance=20)

    df_cleaned = df_merged.query("league_shooting_pct != 0 & league_shooting_pct != 1")
    df_cleaned = df_cleaned.query("team_shooting_pct != 0 & team_shooting_pct != 1")

    df_cleaned['shooting_percentage_from_average'] = df_cleaned['team_shooting_pct'] - df_cleaned['league_shooting_pct']
    df_cleaned['x'] = df_cleaned['coordinate'] % 10000
    df_cleaned['y'] = (df_cleaned['coordinate'] / 10000)
    

    hexbin_diff = ax.hexbin(df_cleaned["y"], df_cleaned["x"],C=df_cleaned['shooting_percentage_from_average'], gridsize=20, cmap="coolwarm")
    plt.colorbar(hexbin_diff, label='Shooting Relative to League Average')
    plt.show()

    hexbin_l.remove()
    hexbin_t.remove()

    return fig

def reduce_hexbins(array):
    total_made_shots = sum(array)
    total_shot_attempts = len(array)

    return total_made_shots / total_shot_attempts