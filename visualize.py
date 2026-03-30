import plotly.express as px
import plotly.io as pio

pio.renderers.default = 'browser'

def shot_distribution_by_year(shot_distribution_df):
    fig= px.bar(shot_distribution_df, x="year", y="shot_count", color="action_type", title="Shot Distribution By Year",hover_name="team_tricode", pattern_shape="team_tricode")
    return fig

def top_playmaker_by_period(top_playmakers_df):
    fig= px.bar(top_playmakers_df, x="period", y="play_quantity", color="play_result", title="Dunk and 3s Assist Leaders by Period",facet_row="player_name")
    return fig