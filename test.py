import streamlit as st
import pandas as pd
import plotly.express as px
from lolesports_api import League

# =============================
# LCK 리그 데이터 불러오기
# =============================
league = League("LCK")
tournament = league.getTournamentBySlug("lck_2025_summer")  # 대회 슬러그 (예: LCK 2025 Summer)
tournament.download()

# 경기 리스트 불러오기
events = tournament.events
event_names = [e.name for e in events]

# =============================
# Streamlit UI
# =============================
st.set_page_config(page_title="LCK 대시보드", layout="wide")
st.title("🎮 LCK 2025 Summer 데이터 대시보드")

# 경기 선택
selected_event = st.selectbox("경기를 선택하세요:", event_names)
event = [e for e in events if e.name == selected_event][0]

# 첫 번째 게임 데이터 가져오기
game = event.games[0]
game.download()
game.loadData()
game.parseData()

# =============================
# 데이터 테이블
# =============================
# 블루팀 & 레드팀 선수별 데이터
blue_team = pd.DataFrame([vars(game.blue.top), vars(game.blue.jungle),
                          vars(game.blue.mid), vars(game.blue.bottom),
                          vars(game.blue.support)])
red_team = pd.DataFrame([vars(game.red.top), vars(game.red.jungle),
                         vars(game.red.mid), vars(game.red.bottom),
                         vars(game.red.support)])

st.subheader("📊 블루팀 선수 스탯")
st.dataframe(blue_team)

st.subheader("📊 레드팀 선수 스탯")
st.dataframe(red_team)

# =============================
# 시각화 (예: KDA 비교)
# =============================
blue_team["Team"] = "Blue"
red_team["Team"] = "Red"
df_all = pd.concat([blue_team, red_team])

fig = px.bar(df_all, x="summonerName", y="kda", color="Team",
             title="선수별 KDA 비교")
st.plotly_chart(fig, use_container_width=True)
