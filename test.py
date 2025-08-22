import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="LoL E-Sports Dashboard", layout="wide")

st.title("🎮 League of Legends E-Sports Dashboard")
st.markdown("Oracle’s Elixir 데이터를 활용한 **실제 프로 경기 분석** 대시보드")

# -----------------------------
# 데이터 업로드 / 불러오기
# -----------------------------
st.sidebar.header("데이터 불러오기")
uploaded_file = st.sidebar.file_uploader("Oracle’s Elixir CSV 업로드", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ 데이터 로드 완료!")

    # -----------------------------
    # 필터 옵션
    # -----------------------------
    st.sidebar.header("필터")
    seasons = df["season"].unique()
    selected_season = st.sidebar.selectbox("시즌 선택", seasons)

    teams = df["team"].unique()
    selected_team = st.sidebar.selectbox("팀 선택", teams)

    filtered = df[(df["season"] == selected_season) & (df["team"] == selected_team)]

    # -----------------------------
    # 기본 정보
    # -----------------------------
    st.subheader(f"📑 {selected_season} 시즌 - {selected_team} 경기 데이터")
    st.write(f"총 경기 수: {len(filtered)}")

    # -----------------------------
    # 승률 계산
    # -----------------------------
    win_rate = filtered["result"].mean() * 100  # Oracle 데이터에서 result = 1이면 승리
    st.metric("승률", f"{win_rate:.1f}%")

    # -----------------------------
    # 평균 K/D/A
    # -----------------------------
    col1, col2, col3 = st.columns(3)
    col1.metric("평균 킬", f"{filtered['kills'].mean():.1f}")
    col2.metric("평균 데스", f"{filtered['deaths'].mean():.1f}")
    col3.metric("평균 어시스트", f"{filtered['assists'].mean():.1f}")

    # -----------------------------
    # 경기별 KDA 그래프
    # -----------------------------
    st.subheader("📊 경기별 킬/데스/어시스트")
    fig, ax = plt.subplots(figsize=(8, 4))
    filtered[["kills", "deaths", "assists"]].reset_index(drop=True).plot(kind="bar", ax=ax)
    plt.title(f"{selected_team} 경기별 KDA")
    plt.xlabel("경기")
    plt.ylabel("수치")
    st.pyplot(fig)

    # -----------------------------
    # 원본 데이터 확인
    # -----------------------------
    with st.expander("🔍 원본 데이터 보기"):
        st.dataframe(filtered)

else:
    st.info("📥 Oracle’s Elixir 사이트에서 CSV를 다운로드 후 업로드해 주세요.")
    st.markdown("[Oracle’s Elixir 데이터 받기](https://oracleselixir.com/match-data)")
