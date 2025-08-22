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
