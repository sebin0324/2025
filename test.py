import streamlit as st
import pandas as pd

# 페이지 기본 설정
st.set_page_config(page_title="🏆 T1 e스포츠 대시보드", page_icon="🔥", layout="wide")

st.title("🏆 T1 e스포츠 대시보드")
st.markdown("📊 선수 기록, 경기 일정, 하이라이트 영상을 한눈에!")

# -------------------------------
# Mock 데이터 (데모용)
# 실제 데이터는 API 크롤링/연동 필요
# -------------------------------

# 선수 기록 (예시)
player_stats = pd.DataFrame({
    "선수": ["Faker", "Zeus", "Oner", "Gumayusi", "Keria"],
    "KDA": [5.2, 4.8, 4.5, 5.0, 6.1],
    "킬": [120, 98, 85, 110, 60],
    "데스": [30, 32, 35, 28, 20],
    "어시스트": [200, 150, 140, 180, 210]
})

# 경기 일정 (예시)
schedule = pd.DataFrame({
    "날짜": ["2025-08-25", "2025-08-27", "2025-08-30"],
    "경기": ["T1 vs Gen.G", "T1 vs DK", "T1 vs KT"]
})

# 하이라이트 영상 (유튜브 링크)
highlight_url = "https://www.youtube.com/watch?v=YQH1Gd0WQOY"  # Faker 하이라이트 예시

# -------------------------------
# 대시보드 UI
# -------------------------------

st.subheader("📊 선수 기록 (T1)")
st.dataframe(player_stats, use_container_width=True)
st.bar_chart(player_stats.set_index("선수")[["킬", "데스", "어시스트"]])

st.subheader("📅 다가오는 경기 일정")
st.table(schedule)

st.subheader("🎥 T1 하이라이트 영상")
st.video(highlight_url)
