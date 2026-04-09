# streamlit_app.py

import streamlit as st
import visualize as vis
import pandas as pd
from streamlit_dynamic_filters import DynamicFilters
from google.oauth2 import service_account
from google.cloud import bigquery
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="NBA Play-by-Play Dashboard",  # the page title shown in the browser tab
    page_icon=":bar_chart:",  # the page favicon shown in the browser tab
    layout="wide",  # page layout : use the entire screen
)

st.title("NBA Play-by-Play Dashboard :bar_chart::basketball:")

# about dataset section
with st.expander('About NBA Play-by-Play Dataset'):
    st.header("About the NBA Play-by-Play Dataset")
    st.write("""The Play-by-Play dataset includes 5 seasons of play by play data from the 
         cdn.nba.com/static/json/liveData/ api which was gathered by shufinskiy on their github page
          https://github.com/shufinskiy/nba_data/tree/main/datasets. This data includes all plays from regular
         season games only and the year code refers to the first year of a given season ie. year 20 references
         the 20-21 nba season.""")


# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]    
)
client = bigquery.Client(credentials=credentials)
PROJECT_ID = st.secrets['gcp_service_account']['project_id']
DATASET = "nba_pbp_dashboard_raw"
TABLE_PREFIX = f"{PROJECT_ID}.{DATASET}"

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    query_job = client.query(query)
    df = query_job.to_dataframe()
    return df

#This section will provide hexbin shooting percentage and shot distribution for teams/player relative to the league for a given year
with st.expander('NBA Shot Charts'):
     
    #Users must select a year to pull data for
    year = st.selectbox(
    "What year do you want to pull data for?",
    ("20", "21", "22", "23", "24", "25"),
    index=None,
    placeholder="Select year to pull shot charts for...",
    )

    if year != None:
        #We grab every shot attempt from all 3 locations on the floor for the entire year to establish the league data and then merge it into a single dataframe
        df_shot_charts_l = run_query(f"SELECT * FROM `{TABLE_PREFIX}.fct_3pt_data` where year = {year}")
        df_shot_charts2_l = run_query(f"SELECT * FROM `{TABLE_PREFIX}.fct_midrange_data` where year = {year}")
        df_shot_charts3_l = run_query(f"SELECT * FROM `{TABLE_PREFIX}.fct_rim_shooting_data` where year = {year}")

        df_merged_l = pd.concat([df_shot_charts_l,df_shot_charts2_l,df_shot_charts3_l])

        #Creating a dynamic filter on the team
        dynamic_filters_shot_chart_team = DynamicFilters(df_merged_l, filters=['team_tricode'],filters_name='shot_chart_team')
        dynamic_filters_shot_chart_team.display_filters()
        df_team_selection = dynamic_filters_shot_chart_team.filter_df()

        #If a team is selected we can generate the shot charts
        if st.session_state['shot_chart_team']['team_tricode'] != []:
            #Create an is_shot_made column and fill it with the results of the shot (made = 1, missed = 0)
            df_merged_l['is_shot_made'] = np.where(df_merged_l['shot_result'] == 'made', 1, 0)
            df_team_selection['is_shot_made'] = np.where(df_team_selection['shot_result'] == 'made', 1, 0)

            #Create an is_shot_attempt column that is 1/(total shot attempts) which is used for generating shot distribution hexbins
            df_merged_l['is_shot_attempt'] = 1 / len(df_merged_l)
            df_team_selection['is_shot_attempt'] = 1 / len(df_team_selection)

            #Create a dynamic filter on the team dataframe to allow the selection of players
            dynamic_filters_shot_chart_player = DynamicFilters(df_team_selection, filters=['player_name'],filters_name='shot_chart_player')
            dynamic_filters_shot_chart_player.display_filters()

            #Plot the heatmaps for shooting percentage and shot distribution relative to the league for the team
            st.pyplot(vis.shot_chart_percentage(df_merged_l,df_team_selection,year,st.session_state['shot_chart_team']['team_tricode'],'', False))
            st.pyplot(vis.shot_chart_distribution(df_merged_l,df_team_selection,year,st.session_state['shot_chart_team']['team_tricode'],'', False))

            df_player_selection = dynamic_filters_shot_chart_player.filter_df()

            #If a player(s) is selected, generate shot charts
            if st.session_state['shot_chart_player']['player_name'] != []:
                # Drop the is_shot_attempt field since the total count will change and then re-calculate
                df_player_selection.drop(['is_shot_attempt'],axis=1, inplace=True)
                df_player_selection['is_shot_attempt'] = 1 / len(df_player_selection)

                #Plot the heatmaps for shooting percentage and shot distribution relative to the league for the player
                st.pyplot(vis.shot_chart_percentage(df_merged_l,df_player_selection,year,st.session_state['shot_chart_team']['team_tricode'],st.session_state['shot_chart_player']['player_name'], True))
                st.pyplot(vis.shot_chart_distribution(df_merged_l,df_player_selection,year,st.session_state['shot_chart_team']['team_tricode'],st.session_state['shot_chart_player']['player_name'], True))

#This section will generate a line graph showing how the distribution of shot type changes from the earlier parts of the game vs the end of game scenarios over the years    
with st.expander('Lead Changing Shot Distribution in Last 3 minutes and OT vs Rest of Game'):
    df_time_based_shot_distribution = run_query(f"SELECT * FROM `{TABLE_PREFIX}.mrt_lead_changing_shot_distribution_by_time_in_game`")

    #Group query results by game_time (normal or end game) and year
    group_cols = ['game_time', 'year'] 

    # Calculate the sum for each group
    group_sums = df_time_based_shot_distribution.groupby(group_cols)['shot_count'].transform('sum')
    

    # Calculate shot distribution
    df_time_based_shot_distribution['total_by_group'] = group_sums
    df_time_based_shot_distribution['shot_percentage'] = df_time_based_shot_distribution['shot_count'] / df_time_based_shot_distribution['total_by_group']
    df_time_based_shot_distribution['shot_percentage'] = df_time_based_shot_distribution['shot_percentage'].round(4)
    df_time_based_shot_distribution['year'] = df_time_based_shot_distribution['year']
    df_time_based_shot_distribution = df_time_based_shot_distribution.sort_values(by="year")

    # Call visualizer to plot
    st.plotly_chart(vis.time_based_shot_distribution_by_year(df_time_based_shot_distribution),height=500)

#This section will generate a stacked bar chart of the distribution of team shots across 2pt and 3pt over the years
with st.expander('Shot Distribution By Year'):
    df_shot_distribution = run_query(f"SELECT * FROM `{TABLE_PREFIX}.fct_shot_diet_by_team_by_year`")

    #Create dynamic filter based on teams
    dynamic_filters_shot_distribution = DynamicFilters(df_shot_distribution, filters=['team_tricode'], filters_name='shot_distribution')
    dynamic_filters_shot_distribution.display_filters()
    shot_distribution_selection = dynamic_filters_shot_distribution.filter_df()

    #Call visualizer to create plot
    st.plotly_chart(vis.shot_distribution_by_year(shot_distribution_selection))

#This section will show the number of assists on a dunk or 3 pointer that a player generates broken out by period of the game
with st.expander('Playmakers By Period'):
    df_playmakers = run_query(f"SELECT * FROM `{TABLE_PREFIX}.mrt_playmakers` ORDER BY play_quantity DESC")

    #It is possible due to how different spelling of names and players being traded midseason to see duplicate records so we need to drop those.
    df_playmakers_cleaned = df_playmakers.drop_duplicates()

    #Create a filter to allow the selection of the player to look at.
    dynamic_filters_playmakers = DynamicFilters(df_playmakers_cleaned, filters=['player_name'], filters_name='playmakers')
    dynamic_filters_playmakers.display_filters()
    playermakers_selection = dynamic_filters_playmakers.filter_df()

    if st.session_state['playmakers']['player_name'] != []:
        #We are using the facet feature, so we want to allow the plot area to expand each time we add a player
        count = len(st.session_state['playmakers']['player_name'])
        st.plotly_chart(vis.playmaker_by_period(playermakers_selection),height=300*count)

