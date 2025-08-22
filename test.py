import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# 앱 기본 설정
# -------------------------------
st.set_page_config(page_title="e스포츠 올인원 웹앱", page_icon="🏆", layout="wide")

st.title("🏆 e스포츠 올인원 웹앱")
st.markdown("📊 **데이터 분석** + 🧩 **참여형 콘텐츠**를 한 곳에서 즐겨보세요!")

# -------------------------------
# 가짜 데이터 준비
# -------------------------------

# 팀 순위표 데이터
team_data = pd.DataFrame({
    "팀": ["T1", "GEN", "DK", "KT", "HLE"],
    "승리": [15, 13, 10, 8, 6],
    "패배": [3, 5, 8, 10, 12]
})
team_data["승률"] = round(team_data["승리"] / (team_data["승리"] + team_data["패배"]) * 100, 1)

# 선수 스탯 (가짜)
player_stats = {
    "Faker": {"KDA": 5.2, "평균 CS": 315, "대표 챔피언": "Ahri"},
    "Chovy": {"KDA": 6.1, "평균 CS": 328, "대표 챔피언": "Azir"},
    "Ruler": {"KDA": 7.0, "평균 CS": 300, "대표 챔피언": "Xayah"}
}

# 메타 트렌드 데이터
meta_data = pd.DataFrame({
    "챔피언": ["Ahri", "Azir", "Xayah", "Jinx", "Lee Sin"],
    "픽률": [45, 38, 35, 28, 25],
    "밴률": [30, 22, 40, 15, 18]
})

# 스트리머 랭킹 데이터
streamer_data = pd.DataFrame({
    "스트리머": ["FakerTV", "DeftLive", "ChovyCam", "RulerVision", "ShowMaker"],
    "시청자 수": [25000, 18000, 15000, 12000, 9000]
})

# 퀴즈 데이터
quiz_questions = [
    {"question": "LoL에서 최초 월드챔피언십 우승팀은?", "options": ["T1", "Fnatic", "Samsung", "G2"], "answer": "Fnatic"},
    {"question": "발로란트에서 기본 요원이 아닌 것은?", "options": ["Phoenix", "Jett", "Sage", "Yoru"], "answer": "Yoru"},
    {"question": "T1 Faker의 주 포지션은?", "options": ["탑", "정글", "미드", "원딜"], "answer": "미드"}
]

# -------------------------------
# 사이드바 메뉴
# -------------------------------
menu = st.sidebar.radio(
    "메뉴 선택",
    ["홈", "데이터 대시보드", "참여형 콘텐츠"]
)

# -------------------------------
# 홈 화면
# -------------------------------
if menu == "홈":
    st.header("✨ 환영합니다!")
    st.markdown(
        """
        이 앱은 e스포츠 정보를 **데이터 시각화**와  
        **참여형 게임/퀴즈**로 제공합니다 🎮  
        
        👉 왼쪽 메뉴에서 원하는 기능을 선택해보세요!
        """
    )

# -------------------------------
# 데이터 대시보드
# -------------------------------
elif menu == "데이터 대시보드":
    st.header("📊 e스포츠 데이터 대시보드")
    tab1, tab2, tab3 = st.tabs(["팀/리그 통계", "선수 스탯", "메타 트렌드"])
    
    # 팀/리그 통계
    with tab1:
        st.subheader("리그/팀 순위")
        st.dataframe(team_data, use_container_width=True)

        fig, ax = plt.subplots()
        ax.bar(team_data["팀"], team_data["승률"])
        ax.set_ylabel("승률(%)")
        ax.set_title("팀별 승률")
        st.pyplot(fig)
    
    # 선수 스탯
    with tab2:
        st.subheader("선수 스탯 조회")
        player = st.text_input("선수 이름을 입력하세요 (예: Faker, Chovy, Ruler)", "")
        if player in player_stats:
            st.success(f"🎮 {player} 선수의 최근 스탯")
            st.write(player_stats[player])
        elif player:
            st.error("해당 선수 데이터가 없습니다.")
    
    # 메타 트렌드
    with tab3:
        st.subheader("메타 트렌드 (픽률/밴률)")
        st.dataframe(meta_data, use_container_width=True)

        fig, ax = plt.subplots()
        ax.bar(meta_data["챔피언"], meta_data["픽률"], label="픽률")
        ax.bar(meta_data["챔피언"], meta_data["밴률"], bottom=meta_data["픽률"], label="밴률")
        ax.set_ylabel("비율(%)")
        ax.set_title("챔피언 픽률 & 밴률")
        ax.legend()
        st.pyplot(fig)

# -------------------------------
# 참여형 콘텐츠
# -------------------------------
elif menu == "참여형 콘텐츠":
    st.header("🧩 참여형 콘텐츠")
    tab1, tab2 = st.tabs(["e스포츠 퀴즈", "스트리머 랭킹"])
    
    # 퀴즈 게임
    with tab1:
        st.subheader("e스포츠 퀴즈 게임")
        score = 0
        for i, q in enumerate(quiz_questions):
            st.write(f"**Q{i+1}. {q['question']}**")
            choice = st.radio("선택하세요:", q["options"], key=f"q{i}")
            if choice == q["answer"]:
                score += 1
        st.success(f"최종 점수: {score} / {len(quiz_questions)}")
    
    # 스트리머 랭킹
    with tab2:
        st.subheader("실시간 스트리머 랭킹 (데모)")
        st.dataframe(streamer_data, use_container_width=True)

        fig, ax = plt.subplots()
        ax.barh(streamer_data["스트리머"], streamer_data["시청자 수"])
        ax.set_xlabel("시청자 수")
        ax.set_title("스트리머 인기 순위")
        st.pyplot(fig)
