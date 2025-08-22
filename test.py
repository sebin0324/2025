import streamlit as st
import pandas as pd
import plotly.express as px
from lolesports_api import League

# 예: LCK 리그 데이터를 로드하는 방식
league = League('LCK')
tournament = league.getTournamentBySlug('lck_2025_summer')  # 예시 슬러그
tournament.download()  # 데이터 다운로드
event = tournament.getEventByTeamGame('T1', 1)  # 특정 경기를 선택
game = event.getGameByNum(1)
game.download()
game.loadData()
game.parseData()

# 선수 스탯을 DataFrame으로 변환 (예시)
df_players = game.blue.top.data  # 'blue' 팀의 'top' 포지션 데이터

# Streamlit 시각화
st.title("LCK 경기 데이터 대시보드")
st.subheader("Top 포지션 스탯 (블루팀)")
st.dataframe(pd.DataFrame(df_players))
