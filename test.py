import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================
# 샘플 e스포츠 데이터 불러오기 (CSV 대신 코드 내에 직접 작성)
# ==========================
data = {
    'Player': ['Faker', 'Zeus', 'Chovy', 'Peyz', 'Ruler', 'Canyon', 'ShowMaker', 'Viper'],
    'Team': ['T1', 'T1', 'GEN', 'GEN', 'JD', 'DK', 'DK', 'HLE'],
    'Kills': [7, 3, 5, 8, 9, 4, 6, 10],
    'Deaths': [1, 2, 3, 2, 2, 5, 4, 3],
    'Assists': [8, 5, 7, 10, 11, 6, 9, 12]
}

df = pd.DataFrame(data)
df["KDA"] = (df["Kills"] + df["Assists"]) / df["Deaths"]

# ==========================
# Streamlit 앱 시작
# ==========================
st.set_page_config(page_title="LCK Sample Dashboard", layout="wide")

st.title("🎮 LCK Sample Dashboard")
st.markdown("샘플 데이터를 활용한 선수별 경기 스탯 시각화 대시보드입니다.")

# ==========================
# 데이터 테이블
# ==========================
st.subheader("📊 선수별 상세 데이터")
st.dataframe(df)

# ==========================
# 시각화 1: 선수별 KDA 바 차트
# ==========================
fig1 = px.bar(df, x="Player", y="KDA", color="Team", title="선수별 KDA")
st.plotly_chart(fig1, use_container_width=True)

# ==========================
# 시각화 2: 킬/데스/어시스트 분포
# ==========================
fig2 = px.scatter(df, x="Kills", y="Assists", size="KDA", color="Team",
                  hover_name="Player", title="킬 vs 어시스트 (크기: KDA)")
st.plotly_chart(fig2, use_container_width=True)

# ==========================
# 하이라이트 카드
# ==========================
best_player = df.sort_values(by='KDA', ascending=False).iloc[0]
st.markdown(f"### 🏆 최고 KDA 선수: **{best_player['Player']}** ({best_player['KDA']:.1f})")
