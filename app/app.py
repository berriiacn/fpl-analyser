import streamlit as st
import pandas as pd
import requests

# -------------------------
# Page Configuration (MUST BE FIRST)
# -------------------------
st.set_page_config(page_title="FPL Stats Analyser", layout="wide")

# -------------------------
# Load FPL data
# -------------------------
@st.cache_data
def load_data():
    data = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/").json()
    fixtures = requests.get("https://fantasy.premierleague.com/api/fixtures/").json()

    players_df = pd.DataFrame(data['elements'])
    teams_df = pd.DataFrame(data['teams'])
    fixtures_df = pd.DataFrame(fixtures)

    return players_df, teams_df, fixtures_df

players_df, teams_df, fixtures_df = load_data()

# -------------------------
# Page Title
# -------------------------
st.title("⚽ Fantasy Premier League Stats Analyser")

# -------------------------
# Player vs Player Comparison
# -------------------------
st.header("🔍 Player vs Player Comparison")

player_names = players_df['web_name'].sort_values().unique()
col1, col2 = st.columns(2)
p1 = col1.selectbox("Select Player 1", player_names, index=0)
p2 = col2.selectbox("Select Player 2", player_names, index=1)

stats_to_compare = [
    'minutes', 'total_points', 'points_per_game',
    'clean_sheets', 'goals_scored', 'assists', 'bonus'
]

comparison_df = players_df[players_df['web_name'].isin([p1, p2])][['web_name'] + stats_to_compare]
st.dataframe(comparison_df.set_index('web_name'), use_container_width=True)

# -------------------------
# Top Players by Points Per Game
# -------------------------
st.header("🔥 Top 15 Players by Points Per Game")
most_ppg = players_df[['web_name', 'points_per_game', 'now_cost', 'minutes']]\
    .sort_values(by='points_per_game', ascending=False).head(15)
st.dataframe(most_ppg.set_index('web_name'), use_container_width=True)

# -------------------------
# Top Players by Points Per Million
# -------------------------
st.header("💰 Top 15 Players by Points Per Million")
players_df['points_per_million'] = players_df['total_points'] / (players_df['now_cost'] / 10)
points_per_million = players_df[['web_name', 'total_points', 'now_cost', 'points_per_million']]\
    .sort_values(by='points_per_million', ascending=False).head(15)
st.dataframe(points_per_million.set_index('web_name'), use_container_width=True)

# -------------------------
# Top Defenders by Total Points
# -------------------------
st.header("🛡️ Top 10 Defenders by Total Points")
defenders = players_df[players_df['element_type'] == 2]
top_defenders = defenders[['web_name', 'total_points', 'clean_sheets', 'goals_scored', 'assists', 'bonus', 'now_cost']]\
    .sort_values(by='total_points', ascending=False).head(10)
st.dataframe(top_defenders.set_index('web_name'), use_container_width=True)

# -------------------------
# Injury/Flagged Players
# -------------------------
st.header("⚠️ Players with Injury/News Updates")
flagged_players = players_df[players_df['news'].str.len() > 0][['web_name', 'news', 'chance_of_playing_this_round']]
if len(flagged_players) > 0:
    st.dataframe(flagged_players.set_index('web_name'), use_container_width=True)
else:
    st.success("No players currently flagged!")

# -------------------------
# Fixture Difficulty GW1–5
# -------------------------
st.header("📅 Teams with Most Easy Fixtures (GW1–5) (2024/25 season waiting for new API database)")

early_fixtures = fixtures_df[fixtures_df['event'] <= 5]
easy_home = early_fixtures[early_fixtures['team_h_difficulty'] <= 2]['team_h'].value_counts()
easy_away = early_fixtures[early_fixtures['team_a_difficulty'] <= 2]['team_a'].value_counts()
easy_fixtures = (easy_home + easy_away).sort_values(ascending=False)

# Map team IDs to names
team_name_map = dict(zip(teams_df['id'], teams_df['name']))
easy_fixtures.index = easy_fixtures.index.map(team_name_map)

st.dataframe(easy_fixtures.rename("Easy Fixtures").to_frame(), use_container_width=True)

# -------------------------
# Top Defenders by Defensive Contributions
# -------------------------
st.header("🛡️ Top 20 Defenders by Defensive Contributions")
defenders = players_df[players_df['element_type'] == 2]
defenders_defensive_contributions = defenders[['web_name', 'defensive_contribution', 'clearances_blocks_interceptions', 'tackles', 'recoveries', 'minutes']].sort_values(by='defensive_contribution', ascending=False).head(20)
st.dataframe(defenders_defensive_contributions.set_index('web_name'), use_container_width=True)

st.header("🛡️ Top 20 Midfielders by Defensive Contributions")
midfielders = players_df[players_df['element_type'] == 3]
midfielders_defensive_contributions = midfielders[['web_name', 'defensive_contribution', 'clearances_blocks_interceptions', 'tackles', 'recoveries', 'minutes']].sort_values(by='defensive_contribution', ascending=False).head(20)
st.dataframe(midfielders_defensive_contributions.set_index('web_name'), use_container_width=True)