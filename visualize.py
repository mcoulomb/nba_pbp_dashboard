import plotly.express as px
import plotly.io as pio
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
from matplotlib.patches import Circle, Rectangle, Arc

pio.renderers.default = 'browser'


def shot_distribution_by_year(shot_distribution_df):
    fig= px.bar(shot_distribution_df, x="year", y="shot_count", color="action_type", title="Shot Distribution By Year",hover_name="team_tricode", pattern_shape="team_tricode")
    return fig

def playmaker_by_period(playmakers_df):
    fig= px.bar(playmakers_df, x="period", y="play_quantity", color="play_result", title="Dunk and 3s Assist Leaders by Period",facet_row="player_name")
    return fig

def time_based_shot_distribution_by_year(time_based_shot_distribution_df):
    fig = px.line(time_based_shot_distribution_df, x="year", y="shot_percentage", line_dash="game_time", color='shot_type', title="Distribution of Shot Types causing a Lead Change based on Time in Game", color_discrete_sequence=['#FF0000', 'orange', '#0000FF'])
    return fig

def shot_chart_percentage(shot_chart_df_league, shot_chart_df_team,year,team,player, is_player_filter):
    shot_chart_df_l = shot_chart_df_league.copy(deep=True)
    shot_chart_df_t = shot_chart_df_team.copy(deep=True)

    # If we are generating the shot map for a player the minimum shot count for the hexbin should be lower.
    if is_player_filter:
        shot_count_filter = 10
    else:
        shot_count_filter = 50
        
    # Setup initial figure dimensions and add the overlay of the 3 point line and hoop 
    fig, ax = plt.subplots(figsize=(8, 4))
    add_court(ax)

    #Create the hexbins for shot percentage for the league and (team or player)
    hexbin_l = ax.hexbin(shot_chart_df_l["y_location_converted"], shot_chart_df_l["x_location_converted"],C=shot_chart_df_l["is_shot_made"],reduce_C_function=reduce_hexbins_shooting_percentage, gridsize=20, cmap="Reds", mincnt=50)
    hexbin_t = ax.hexbin(shot_chart_df_t["y_location_converted"], shot_chart_df_t["x_location_converted"], gridsize=20,C=shot_chart_df_t["is_shot_made"],reduce_C_function=reduce_hexbins_shooting_percentage, cmap="Reds", mincnt=shot_count_filter)
    ax.set_title(f"Shooting Percentage Heat Map for year:{year} team:{team} players:{player}")

    # We want to convert the x,y coordinates into a single value coordinate using z=(x*10000) + y
    # This will allow us to use merge_asof() to compare the 2 hexbins
    league_array = hexbin_l.get_offsets()

    la, lb = np.hsplit(league_array, 2) 
    la = np.squeeze(la) # array([1, 3, 5])
    lb = np.squeeze(lb) # array([2, 4, 6])

    la = np.round(la,0)
    lb = np.round(lb,0)
    single_value_coordinate_l = (la*10000) + lb

    #Create a dataframe using the single_value_coordinate and shooting percentage for each hexbin
    single_value_array_l = np.column_stack([single_value_coordinate_l, hexbin_l.get_array()])
    df_league = pd.DataFrame(single_value_array_l,columns=["coordinate","league_shooting_pct"])

    team_array = hexbin_t.get_offsets()

    ta, tb = np.hsplit(team_array, 2) 
    ta = np.squeeze(ta) # array([1, 3, 5])
    tb = np.squeeze(tb) # array([2, 4, 6])

    ta = np.round(ta,0)
    tb = np.round(tb,0)
    single_value_coordinate_t = (ta*10000) + tb

    #Create a dataframe using the single_value_coordinate and shooting percentage for each hexbin
    single_value_array_t = np.column_stack([single_value_coordinate_t, hexbin_t.get_array()])
    df_team = pd.DataFrame(single_value_array_t,columns=["coordinate","team_shooting_pct"])

    #Sort dataframes by coordinates
    df_team.sort_values(by="coordinate",inplace=True)
    df_league.sort_values(by="coordinate",inplace=True)

    #Merge the two dataframes together based on the coordinate column and using the nearest values.
    df_merged = pd.merge_asof(df_team,df_league, on=['coordinate'],direction='nearest', tolerance=1000)

    #Remove any rows that have one side or the other shooting 0 percent or 100 percent since they will create noise
    df_cleaned = df_merged.query("league_shooting_pct != 0 & league_shooting_pct != 1")
    df_cleaned = df_cleaned.query("team_shooting_pct != 0 & team_shooting_pct != 1")

    #Get the relative shooting percentage and pull the coordinates out from the single value coordinate.
    df_cleaned['shooting_percentage_from_average'] = df_cleaned['team_shooting_pct'] - df_cleaned['league_shooting_pct']
    df_cleaned['x'] = df_cleaned['coordinate'] % 10000
    df_cleaned['y'] = (df_cleaned['coordinate'] / 10000)
    
    #When there is only a small amouont of data in the dataframe the hexbins don't display properly. We use the number of unique
    # Y values to determine a dynamic gridsize when filtering down to player.
    distinct_values = df_cleaned["y"].unique()
    
    if(is_player_filter):
        gridsize=np.ceil(len(distinct_values)/2).astype(int) + 1
    else:
        gridsize=20

    #Create the hexbin for the Shooting Percentage Relative to League Average and a colorbar to show what the scale is
    hexbin_diff = ax.hexbin(df_cleaned["y"], df_cleaned["x"],C=df_cleaned['shooting_percentage_from_average'], gridsize=gridsize, cmap="coolwarm", vmin=-.15,vmax=.15)
    plt.colorbar(hexbin_diff, label='Shooting Relative to League Average')
    plt.show()

    #Remove the original 2 hexbin plots
    hexbin_l.remove()
    hexbin_t.remove()

    return fig

def shot_chart_distribution(shot_chart_df_league, shot_chart_df_team,year,team,player, is_player_filter):
    shot_chart_df_l = shot_chart_df_league.copy(deep=True)
    shot_chart_df_t = shot_chart_df_team.copy(deep=True)
    
    # If we are generating the shot map for a player the minimum shot count for the hexbin should be lower.
    if is_player_filter:
        min_shot_count_filter = 10
    else:
        min_shot_count_filter = 50
        
    # Setup initial figure dimensions and add the overlay of the 3 point line and hoop    
    fig, ax = plt.subplots(figsize=(8, 4))
    add_court(ax)

    #Create the hexbins for shot distribution for the league and (team or player)
    hexbin_l = ax.hexbin(shot_chart_df_l["y_location_converted"], shot_chart_df_l["x_location_converted"],C=shot_chart_df_l["is_shot_attempt"],reduce_C_function=reduce_hexbins_shot_distribution, gridsize=20, cmap="Reds", mincnt=50)
    hexbin_t = ax.hexbin(shot_chart_df_t["y_location_converted"], shot_chart_df_t["x_location_converted"],C=shot_chart_df_t["is_shot_attempt"],reduce_C_function=reduce_hexbins_shot_distribution, gridsize=20, cmap="Reds", mincnt=min_shot_count_filter)
    ax.set_title(f"Shooting Distribution Heat Map for year:{year} team:{team} players:{player}")

    # We want to convert the x,y coordinates into a single value coordinate using z=(x*10000) + y
    # This will allow us to use merge_asof() to compare the 2 hexbins
    league_array = hexbin_l.get_offsets()

    la, lb = np.hsplit(league_array, 2) 
    la = np.squeeze(la)
    lb = np.squeeze(lb) 

    la = np.round(la,0)
    lb = np.round(lb,0)
    single_value_coordinate_l = (la*10000) + lb

    #Create a dataframe using the single_value_coordinate and shot distribution for each hexbin
    single_value_array_l = np.column_stack([single_value_coordinate_l, hexbin_l.get_array()])
    df_league = pd.DataFrame(single_value_array_l,columns=["coordinate","league_shooting_distribution"])

    team_array = hexbin_t.get_offsets()

    ta, tb = np.hsplit(team_array, 2) 
    ta = np.squeeze(ta)
    tb = np.squeeze(tb)

    ta = np.round(ta,0)
    tb = np.round(tb,0)
    single_value_coordinate_t = (ta*10000) + tb

    #Create a dataframe using the single_value_coordinate and shot distribution for each hexbin
    single_value_array_t = np.column_stack([single_value_coordinate_t, hexbin_t.get_array()])
    df_team = pd.DataFrame(single_value_array_t,columns=["coordinate","team_shooting_distribution"])

    #Sort dataframes by coordinates
    df_team.sort_values(by="coordinate",inplace=True)
    df_league.sort_values(by="coordinate",inplace=True)

    #Merge the two dataframes together based on the coordinate column and using the nearest values.
    df_merged = pd.merge_asof(df_team,df_league, on=['coordinate'],direction='nearest')

    #Remove any rows that have one side or the other shooting 0 percent or 100 percent since they will create noise
    df_cleaned = df_merged.query("league_shooting_distribution != 0 & league_shooting_distribution != 1")
    df_cleaned = df_cleaned.query("team_shooting_distribution != 0 & team_shooting_distribution != 1")

    #Get the relative shot distribution and pull the coordinates out from the single value coordinate.
    df_cleaned['shooting_distribution_difference'] = df_cleaned['team_shooting_distribution'] - df_cleaned['league_shooting_distribution']
    df_cleaned['x'] = (df_cleaned['coordinate'] % 10000).astype(int)
    df_cleaned['y'] = (df_cleaned['coordinate'] / 10000).astype(int)
    
    #When there is only a small amouont of data in the dataframe the hexbins don't display properly. We use the number of unique
    # Y values to determine a dynamic gridsize when filtering down to player.
    distinct_values = df_cleaned["y"].unique()

    if(is_player_filter):
        gridsize=np.ceil(len(distinct_values)/2).astype(int) + 1
    else:
        gridsize=20

    #Create the hexbin for the Shot Selection Relative to League Average and a colorbar to show what the scale is
    hexbin_diff = ax.hexbin(df_cleaned["y"], df_cleaned["x"],C=df_cleaned['shooting_distribution_difference'], cmap="coolwarm",gridsize=gridsize, vmin=-.05,vmax=.05)
    plt.colorbar(hexbin_diff, label='Shot Selection Relative to League Average')
    plt.show()

    #Remove the original 2 hexbin plots
    hexbin_l.remove()
    hexbin_t.remove()

    return fig

#The C value for each row in the hexbin is either 1 or 0. So below we take the sum of shots made (sum(array))
#and divide it by the total number of shot attempts of the (league/team/players) to get the shooting percentage from that hexbin.
def reduce_hexbins_shooting_percentage(array):
    total_made_shots = sum(array)
    total_shot_attempts = len(array)

    return total_made_shots / total_shot_attempts

#The C value for each shot attempt in a hexbin is 1/(total shots attempted) so the sum should be 
# what percent of the (league/team/players) shots come from that hexbin
def reduce_hexbins_shot_distribution(array):
    return sum(array)

def add_court(ax):
    # Three point line
    # Side 3pt lines (straight segments)
    corner_three_a = Rectangle((3, 0), 0, 14, linewidth=2, color='black')
    corner_three_b = Rectangle((47, 0), 0, 14, linewidth=2, color='black')
    
    # 3pt arc (curved segment)
    # Center at hoop (25,5), radius 23'9", theta1=22, theta2=158
    three_arc = Arc((25, 5),47.5,47.5, theta1=22, theta2=158, linewidth=2, color='black')

    hoop = Circle((25,4),2,fill=False, edgecolor='black', linewidth=2)
    
    # Add elements to the axes
    court_elements = [corner_three_a, corner_three_b, three_arc, hoop]
    for element in court_elements:
        ax.add_patch(element)