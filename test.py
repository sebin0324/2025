import streamlit as st

# 앱 설정
st.set_page_config(page_title="e스포츠 밈 생성기", page_icon="🎮", layout="centered")

st.title("🎤 e스포츠 밈 생성기")
st.markdown("원하는 **선수 이름 + 밈 문구**를 입력하고 나만의 e스포츠 밈을 만들어보세요!")

# 입력창
player = st.text_input("선수 이름을 입력하세요 (예: Faker, Chovy, Ruler)")
meme_text = st.text_area("밈 문구를 입력하세요 (예: 나는 아직도 배고프다)")

# 버튼
if st.button("밈 생성하기 ✨"):
    if player and meme_text:
        st.success("✅ 밈이 생성되었습니다!")

        # 카드 스타일 출력
        st.markdown(
            f"""
            <div style="border-radius:15px; padding:20px; background-color:#1e1e2f; color:white; text-align:center; box-shadow:2px 2px 10px gray;">
                <h2>🏆 {player}</h2>
                <p style="font-size:20px; font-style:italic;">"{meme_text}"</p>
                <hr>
                <p>🔥 The Unkillable Legend</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.error("⚠️ 선수 이름과 밈 문구를 모두 입력해주세요!")

# 랜덤 밈 추천
import random
sample_memes = [
    "나는 아직도 배고프다",
    "드래곤은 내꺼야",
    "팀워크 makes the dream work",
    "바론은 우리 거야!",
    "지금부터가 진짜 경기다"
]

if st.button("랜덤 밈 추천 🎲"):
    random_meme = random.choice(sample_memes)
    st.info(f"💡 추천 밈 문구: **{random_meme}**")
