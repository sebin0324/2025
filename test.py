import streamlit as st
import pandas as pd

# 페이지 기본 설정
st.set_page_config(page_title="⚽ 스포츠 데이터 대시보드", page_icon="⚽", layout="wide")

st.title("⚽ 스포츠 데이터 대시보드")
st.markdown("K리그 & 프리미어리그 순위, 선수 기록, 경기 일정, 하이라이트를 한눈에!")

# 리그 선택
league = st.sidebar.selectbox("리그 선택", ["프리미어리그", "K리그"])

# -------------------------------
# Mock 데이터 생성
# -------------------------------
if league == "프리미어리그":
    # 순위표
    standings = pd.DataFrame({
        "순위": [1, 2, 3, 4, 5],
        "팀": ["맨시티", "리버풀", "아스날", "토트넘", "첼시"],
        "승점": [75, 72, 70, 65, 60],
        "승": [24, 22, 21, 20, 18],
        "무": [3, 6, 7, 5, 6],
        "패": [5, 4, 5, 7, 10]
    })

    # 선수 기록 (득점왕 TOP 5)
    top_scorers = pd.DataFrame({
        "선수": ["홀란드", "살라", "손흥민", "사카", "누녜스"],
        "득점": [26, 22, 20, 18, 17]
    })

    # 경기 일정
    schedule = pd.DataFrame({
        "날짜": ["2025-08-25", "2025-08-26", "2025-08-27"],
        "경기": ["맨시티 vs 아스날", "리버풀 vs 첼시", "토트넘 vs 뉴캐슬"]
    })

    # 하이라이트 링크
    highlight_url = "https://www.youtube.com/watch?v=mf0kqNRt3pM"  # EPL Highlights

else:  # K리그
    # 순위표
    standings = pd.DataFrame({
        "순위": [1, 2, 3, 4, 5],
        "팀": ["울산", "포항", "서울", "전북", "인천"],
        "승점": [62, 59, 55, 52, 48],
        "승": [19, 18, 16, 15, 13],
        "무": [5, 5, 7, 7, 9],
        "패": [4, 5, 6, 8, 9]
    })

    # 선수 기록 (득점왕 TOP 5)
    top_scorers = pd.DataFrame({
        "선수": ["주니오", "이승우", "조규성", "무고사", "나상호"],
        "득점": [21, 18, 16, 15, 14]
    })

    # 경기 일정
    schedule = pd.DataFrame({
        "날짜": ["2025-08-25", "2025-08-26", "2025-08-27"],
        "경기": ["울산 vs 전북", "서울 vs 인천", "포항 vs 강원"]
    })

    # 하이라이트 링크
    highlight_url = "https://www.youtube.com/watch?v=fL3rUqYv4Ug"  # K리그 Highlights

# -------------------------------
# 대시보드 UI
# -------------------------------
st.subheader(f"📊 {league} 순위표")
st.dataframe(standings, use_container_width=True)
st.bar_chart(standings.set_index("팀")["승점"])

st.subheader("🥅 득점왕 TOP 5")
st.dataframe(top_scorers, use_container_width=True)
st.bar_chart(top_scorers.set_index("선수"))

st.subheader("📅 다가오는 경기 일정")
st.table(schedule)

st.subheader("🎥 하이라이트 영상")
st.video(highlight_url)
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import random

# 앱 설정
st.set_page_config(page_title="e스포츠 밈 생성기", page_icon="🎮", layout="centered")

st.title("🎤 e스포츠 밈 생성기")
st.markdown("**선수 이름 + 밈 문구**를 입력하면 자동으로 밈 이미지를 생성합니다!")

# 입력창
player = st.text_input("선수 이름을 입력하세요 (예: Faker, Chovy, Ruler)")
meme_text = st.text_area("밈 문구를 입력하세요 (예: 나는 아직도 배고프다)")

# 랜덤 밈 추천
sample_memes = [
    "나는 아직도 배고프다",
    "드래곤은 내꺼야",
    "팀워크 makes the dream work",
    "바론은 우리 거야!",
    "지금부터가 진짜 경기다"
]
if st.button("랜덤 밈 추천 🎲"):
    meme_text = random.choice(sample_memes)
    st.info(f"💡 추천 밈 문구: **{meme_text}**")

# 이미지 생성 버튼
if st.button("밈 이미지 생성하기 ✨"):
    if player and meme_text:
        # 이미지 캔버스 생성
        img = Image.new("RGB", (600, 400), color=(30, 30, 50))
        draw = ImageDraw.Draw(img)

        # 폰트 설정 (기본 폰트 사용)
        try:
            font_title = ImageFont.truetype("arial.ttf", 40)
            font_text = ImageFont.truetype("arial.ttf", 28)
            font_sub = ImageFont.truetype("arial.ttf", 20)
        except:
            font_title = ImageFont.load_default()
            font_text = ImageFont.load_default()
            font_sub = ImageFont.load_default()

        # 텍스트 추가
        draw.text((200, 30), f"🏆 {player}", fill=(255, 215, 0), font=font_title)
        draw.text((50, 150), f"\"{meme_text}\"", fill=(255, 255, 255), font=font_text)
        draw.text((200, 350), "🔥 The Unkillable Legend", fill=(200, 200, 200), font=font_sub)

        # Streamlit에 출력
        st.image(img, caption="생성된 밈 이미지", use_container_width=False)

        # 다운로드용 버퍼
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        byte_im = buf.getvalue()

        st.download_button(
            label="📥 밈 이미지 다운로드",
            data=byte_im,
            file_name="meme.png",
            mime="image/png"
        )

    else:
        st.error("⚠️ 선수 이름과 밈 문구를 모두 입력해주세요!")
