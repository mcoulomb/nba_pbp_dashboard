import plotly.express as px
import plotly.io as pio
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import numpy as np

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

def shot_chart(shot_chart_df):
# Create hexbin mapbox using figure_factory
    fig, ax = plt.subplots()
    ax.hexbin(shot_chart_df["y_location_converted"], shot_chart_df["x_location_converted"], gridsize=75, C=shot_chart_df['is_shot_made'], reduce_C_function=np.mean, cmap="Reds")
    ax.set_title('Hexbin Chart')
    
    return fig