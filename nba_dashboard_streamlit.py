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

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    query_job = client.query(query)
    df = query_job.to_dataframe()
    return df


with st.expander('Lead Changing Shot Distribution in Last 3 minutes and OT vs Rest of Game'):
    df_time_based_shot_distribution = run_query("SELECT * FROM `nba-pbp-dashboard.nba_pbp_dashboard_raw.mrt_lead_changing_shot_distribution_by_time_in_game`")
    # Define the column(s) that define the matching attributes
    # Example: group by 'category'
    group_cols = ['game_time', 'year'] 

    # Calculate the sum for each group
    group_sums = df_time_based_shot_distribution.groupby(group_cols)['shot_count'].transform('sum')
    

    # Assign the result to a new column
    df_time_based_shot_distribution['total_by_group'] = group_sums
    df_time_based_shot_distribution['shot_percentage'] = df_time_based_shot_distribution['shot_count'] / df_time_based_shot_distribution['total_by_group']
    df_time_based_shot_distribution['shot_percentage'] = df_time_based_shot_distribution['shot_percentage'].round(4)
    df_time_based_shot_distribution['year'] = df_time_based_shot_distribution['year'].astype(int)
    df_time_based_shot_distribution = df_time_based_shot_distribution.sort_values(by="year")
    st.plotly_chart(vis.time_based_shot_distribution_by_year(df_time_based_shot_distribution),height=500)

with st.expander('Shot Distribution By Year'):
    df_shot_distribution = run_query("SELECT * FROM `nba-pbp-dashboard.nba_pbp_dashboard_raw.fct_shot_diet_by_team_by_year`")
    dynamic_filters_shot_distribution = DynamicFilters(df_shot_distribution, filters=['team_tricode'], filters_name='shot_distribution')
    dynamic_filters_shot_distribution.display_filters()
    shot_distribution_selection = dynamic_filters_shot_distribution.filter_df()
    st.plotly_chart(vis.shot_distribution_by_year(shot_distribution_selection))

#with st.expander('Top Playmakers By Period'):
    #df_top_playmakers = run_query("SELECT * FROM `nba-pbp-dashboard.nba_pbp_dashboard_raw.fct_top_playmakers` ORDER BY play_quantity DESC")
    #df_playmakers_cleaned = df_top_playmakers.drop_duplicates()
    #dynamic_filters_top_playmakers = DynamicFilters(df_playmakers_cleaned, filters=['player_name'], filters_name='top_playmakers')
    #dynamic_filters_top_playmakers.display_filters()
    #top_playermakers_selection = dynamic_filters_top_playmakers.filter_df()
    #if st.session_state['top_playmakers']['player_name'] != []:
        #count = len(st.session_state['top_playmakers']['player_name'])
        #st.plotly_chart(vis.top_playmaker_by_period(top_playermakers_selection),height=300*count)

with st.expander('NBA Player Shot Charts'):
    df_shot_charts = run_query("SELECT * FROM `nba-pbp-dashboard.nba_pbp_dashboard_raw.fct_3pt_data` where year = '24' and team_tricode = 'nyk' ")
    df_shot_charts2 = run_query("SELECT * FROM `nba-pbp-dashboard.nba_pbp_dashboard_raw.fct_midrange_data` where year = '24' and team_tricode = 'nyk' ")
    df_shot_charts3 = run_query("SELECT * FROM `nba-pbp-dashboard.nba_pbp_dashboard_raw.fct_rim_shooting_data` where year = '24' and team_tricode = 'nyk' ")

    df_merged = pd.concat([df_shot_charts,df_shot_charts2,df_shot_charts3])
    print(df_shot_charts)

    df_merged['is_shot_made'] = np.where(df_merged['shot_result'] == 'made', 1, 0)
    #kernel = stats.gaussian_kde([df_shot_charts.is_shot_made])
    #df_shot_charts['z'] = kernel([df_shot_charts.is_shot_made])
    print(df_merged)
    st.pyplot(vis.shot_chart(df_merged))