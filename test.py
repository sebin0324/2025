# Streamlit 해외여행 가이드/추천 앱

아래 두 파일을 같은 폴더에 저장해 실행하세요.

* `app.py`
* `requirements.txt`

터미널에서:

```bash
pip install -r requirements.txt
streamlit run app.py
```

환경변수(필수):

* `GOOGLE_MAPS_API_KEY` : Google Places API 키 (Places API, Geocoding API 활성화)

---

## app.py

```python
import os
import math
import time
import json
from typing import Dict, List, Optional, Tuple

import streamlit as st
import pandas as pd

# Google Maps
try:
    import googlemaps
except Exception as e:
    googlemaps = None

# ------------------------------
# 유틸
# ------------------------------
@st.cache_data(show_spinner=False)
def geocode_city(gmaps, city_country: str) -> Optional[Tuple[float, float]]:
    try:
        res = gmaps.geocode(city_country)
        if not res:
            return None
        loc = res[0]["geometry"]["location"]
        return (loc["lat"], loc["lng"])
    except Exception:
        return None

@st.cache_data(show_spinner=False)
def places_search_text(gmaps, query: str) -> List[dict]:
    out = []
    try:
        res = gmaps.places(query)
        out.extend(res.get("results", []))
        # next_page_token 처리
        while res.get("next_page_token") and len(out) < 60:
            time.sleep(2)
            res = gmaps.places(query, page_token=res["next_page_token"])
            out.extend(res.get("results", []))
    except Exception:
        pass
    return out

@st.cache_data(show_spinner=False)
def places_nearby(gmaps, location: Tuple[float, float], radius: int, keyword: Optional[str] = None, type_: Optional[str] = None):
    out = []
    try:
        res = gmaps.places_nearby(location=location, radius=radius, keyword=keyword, type=type_)
        out.extend(res.get("results", []))
        while res.get("next_page_token") and len(out) < 60:
            time.sleep(2)
            res = gmaps.places_nearby(location=location, radius=radius, keyword=keyword, type=type_, page_token=res["next_page_token"])
            out.extend(res.get("results", []))
    except Exception:
        pass
    return out

# 가중 정렬 키 (평점 * log(리뷰수+1))
def sort_key_rating(place: dict) -> float:
    r = place.get("rating", 0.0)
    n = place.get("user_ratings_total", 0)
    return r * math.log(n + 1)

# 지도 링크 생성
def google_map_link(place_id: str) -> str:
    return f"https://www.google.com/maps/place/?q=place_id:{place_id}"

# ------------------------------
# 나라별 지식 베이스 (간단 샘플)
# 실제 사용 시 자유롭게 확장하세요.
# ------------------------------
COUNTRY_KB: Dict[str, dict] = {
    "일본": {
        "위생": [
            "공공장소 청결도가 매우 높음",
            "식당/상점 손소독제 비치가 일반적",
            "분리수거 철저 (쓰레기통 적음)"
        ],
        "문화": [
            "실내에서 큰 소리로 통화/통행 방해는 실례",
            "현금 결제를 선호하는 소규모 가게 여전히 존재",
            "온천 이용 시 문신, 세정 예절 숙지"
        ],
        "지켜야할_예절": [
            "에스컬레이터 한 줄 서기 (지역마다 방향 다름)",
            "대중교통 내 통화/취식 자제",
            "쓰레기 되가져가기 (특히 길거리)"
        ],
        "불편한점": [
            "쓰레기통이 적어 휴지/봉투 지참 필요",
            "영어 안내가 지역에 따라 부족할 수 있음",
            "피크 시즌 관광지 과밀/대기열 김"
        ],
        "대표도시": ["도쿄", "오사카", "교토", "삿포로", "후쿠오카"],
        "소도시_추천_키워드": ["온천", "성", "전통거리"]
    },
    "태국": {
        "위생": ["대도시 대비 지방은 식수/위생 주의", "길거리 음식 위생 상태 점검 후 이용"],
        "문화": ["사원 방문 시 노출 적은 복장", "머리 쓰다듬기는 실례"],
        "지켜야할_예절": ["왕실 관련 우상/초상 경의 표하기", "신발 벗고 실내 출입 요구 많음"],
        "불편한점": ["더위/습도 높음", "교통 체증", "택시 바가지 일부"],
        "대표도시": ["방콕", "치앙마이", "푸켓"],
        "소도시_추천_키워드": ["전통시장", "야외사원", "자연경관"]
    },
    "베트남": {
        "위생": ["수돗물 음용 지양", "길거리 음식은 붐비는 곳 선택"],
        "문화": ["호칭/존댓말 중요", "사원 사진 촬영 매너"],
        "지켜야할_예절": ["횡단보도 외 무단횡단 주의", "오토바이 도로 안전"],
        "불편한점": ["오토바이 소음/매연", "교통 혼잡", "시내 이동 시 소매치기 주의"]
    },
    "대만": {
        "위생": ["노점도 비교적 위생적이나 선택 필요", "수돗물 끓여 마시기 권장"],
        "문화": ["현금/카드 병행", "지하철 내 음식 금지"],
        "지켜야할_예절": ["쓰레기 분리/시간 준수", "줄 서기 문화 철저"],
        "불편한점": ["여름 더위", "피크타임 혼잡", "폭우 시즌"]
    },
    "싱가포르": {
        "위생": ["도시 전체 청결 엄격 관리", "벌금 규정 다양"],
        "문화": ["다문화 존중", "껌 반입/판매 제한"],
        "지켜야할_예절": ["금연구역 엄격", "대중교통 예절 철저"],
        "불편한점": ["물가 높음", "실내외 온도차 큼", "벌금 규정 주의"]
    },
    "프랑스": {
        "위생": ["식당 위생 전반 양호", "수돗물 음용 가능"],
        "문화": ["기본적인 프랑스어 인사 선호", "지하철 에티켓"],
        "지켜야할_예절": ["상점 인사/작별 예의", "시간약속 중시"],
        "불편한점": ["소매치기 주의", "파업/운행중단 빈발", "영업시간 제한"]
    },
}

# ------------------------------
# 만족도 점수(예시)
# - 관광지 상위 N개와 음식점 상위 N개의 평점/리뷰수를 가중 평균
# ------------------------------

def compute_satisfaction(attractions: List[dict], restaurants: List[dict]) -> float:
    def avg_weighted(items: List[dict]) -> float:
        if not items:
            return 0
        s = 0.0
        w = 0.0
        for it in items:
            r = it.get("rating", 0.0)
            n = it.get("user_ratings_total", 0)
            weight = math.log(n + 1)
            s += r * weight
            w += weight
        return s / w if w > 0 else 0

    a = avg_weighted(attractions)
    b = avg_weighted(restaurants)
    # 관광=60%, 음식=40%
    score = 0.6 * a + 0.4 * b
    return round(score, 2)

# ------------------------------
# UI
# ------------------------------
st.set_page_config(page_title="해외여행 추천 · 위생 · 문화 가이드", page_icon="✈️", layout="wide")

st.title("✈️ 해외여행 추천 · 음식 · 문화 · 위생 올인원")
st.caption("Google Places API를 활용한 실제 평점 기반 추천. 나라별 예절/위생/주의사항은 요약 가이드로 제공됩니다.")

api_key = os.getenv("GOOGLE_MAPS_API_KEY", "")
if not api_key:
    st.warning("환경변수 GOOGLE_MAPS_API_KEY 가 설정되어 있지 않습니다. 일부 기능이 동작하지 않을 수 있어요.")

if googlemaps is None and api_key:
    st.error("googlemaps 패키지가 설치되지 않았습니다. requirements.txt로 설치 후 다시 시도하세요.")

gmaps = googlemaps.Client(key=api_key) if (api_key and googlemaps) else None

# 입력 영역
colA, colB, colC = st.columns([1.3, 1, 1])
with colA:
    country = st.selectbox("나라 선택", sorted(COUNTRY_KB.keys()))
with colB:
    default_city = COUNTRY_KB.get(country, {}).get("대표도시", [""])[0] if COUNTRY_KB.get(country) else ""
    city = st.text_input("주요 도시 (예: 도쿄, 파리)", value=default_city)
with colC:
    show_small_towns = st.checkbox("주요 도시 주변 소도시 추천 포함", value=True)

interest = st.multiselect(
    "관심사(추천 정밀도 향상)",
    ["미술관", "박물관", "자연경관", "전통거리", "온천", "성", "해변", "사원", "카페", "바"] ,
    default=["박물관", "전통거리"]
)

search_btn = st.button("🔎 추천 보기", use_container_width=True)

if search_btn:
    if not (gmaps and city and country):
        st.error("API 키, 나라, 도시를 확인해주세요.")
        st.stop()

    with st.spinner("도시 좌표 확인 중..."):
        latlng = geocode_city(gmaps, f"{city}, {country}")

    if not latlng:
        st.error("도시를 찾을 수 없습니다. 표기(로마자/현지어)를 바꿔 다시 시도해보세요.")
        st.stop()

    # 관광지 수집
    with st.spinner("관광지 검색 중..."):
        attractions = []
        # 기본: tourist_attraction
        nearby = places_nearby(gmaps, latlng, radius=15000, type_="tourist_attraction")
        attractions.extend(nearby)
        # 관심사 키워드
        for kw in interest:
            more = places_nearby(gmaps, latlng, radius=20000, keyword=kw)
            attractions.extend(more)
        # 정렬 및 중복 제거
        seen = set()
        uniq = []
        for p in sorted(attractions, key=sort_key_rating, reverse=True):
            pid = p.get("place_id")
            if pid and pid not in seen:
                seen.add(pid)
                uniq.append(p)
        attractions = uniq[:20]

    # 음식점 Top 3 (평점 + 리뷰수)
    with st.spinner("음식점 추천 중..."):
        foods = places_nearby(gmaps, latlng, radius=5000, type_="restaurant")
        foods = sorted(foods, key=sort_key_rating, reverse=True)[:3]

    # 소도시 제안: 'town' 키워드 인근 텍스트 검색 + 행정구역 레벨 탐색
    small_towns = []
    if show_small_towns:
        with st.spinner("주변 소도시 탐색 중..."):
            q = f"towns near {city} {country}"
            cand = places_search_text(gmaps, q)
            # locality 중심 후보만 추림
            for c in cand:
                types = c.get("types", [])
                if any(t in types for t in ["locality", "sublocality", "administrative_area_level_3"]):
                    small_towns.append(c)
            # 보정: 관광 키워드 기반도 추가
            if not small_towns:
                for kw in COUNTRY_KB.get(country, {}).get("소도시_추천_키워드", []):
                    cand2 = places_search_text(gmaps, f"{kw} near {city} {country}")
                    small_towns.extend(cand2)
            # 정렬/상위 노출
            small_towns = sorted(small_towns, key=sort_key_rating, reverse=True)[:6]

    # 만족도 점수 계산
    score = compute_satisfaction(attractions, foods)

    # ---------------- UI 출력 ----------------
    st.subheader(f"🇺🇳 {country} · {city} 여행 요약")
    st.metric(label="예상 만족도(가중 평균)", value=f"{score} / 5.0")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🏛️ 볼거리 Top 추천")
        if attractions:
            df_attr = pd.DataFrame([
                {
                    "이름": p.get("name"),
                    "평점": p.get("rating", None),
                    "리뷰수": p.get("user_ratings_total", 0),
                    "주소": p.get("vicinity") or p.get("formatted_address"),
                    "지도": google_map_link(p.get("place_id", "")),
                }
                for p in attractions[:10]
            ])
            st.dataframe(df_attr, use_container_width=True, hide_index=True)
        else:
            st.info("관광지 데이터를 찾지 못했습니다.")

    with col2:
        st.markdown("### 🍽️ 음식점 Top 3 (Google 평점 기준)")
        if foods:
            for i, f in enumerate(foods, 1):
                st.markdown(
                    f"**{i}. {f.get('name')}** — 평점 {f.get('rating', 'N/A')} / 리뷰 {f.get('user_ratings_total', 0)}  ")
                st.markdown(f"📍 {f.get('vicinity') or f.get('formatted_address', '')}")
                st.markdown(f"[구글지도 열기]({google_map_link(f.get('place_id',''))})")
                st.divider()
        else:
            st.info("음식점 데이터를 찾지 못했습니다.")

    if show_small_towns:
        st.markdown("### 🏘️ 주변 소도시/근교 후보")
        if small_towns:
            df_town = pd.DataFrame([
                {
                    "이름": t.get("name"),
                    "유형": ", ".join(t.get("types", [])[:3]),
                    "평점": t.get("rating", None),
                    "리뷰수": t.get("user_ratings_total", 0),
                    "지도": google_map_link(t.get("place_id", "")),
                }
                for t in small_towns
            ])
            st.dataframe(df_town, use_container_width=True, hide_index=True)
        else:
            st.info("주변 소도시 추천 결과가 부족합니다. 키워드/도시를 바꿔보세요.")

    st.markdown("### 🧼 위생 · 🧭 문화 · ✅ 지켜야 할 예절 · 😕 불편한 점 (요약)")
    kb = COUNTRY_KB.get(country, {})

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**🧼 위생**")
        st.markdown("\n".join([f"- {x}" for x in kb.get("위생", [])]) or "- 자료 준비 중")
        st.markdown("**🧭 문화(일반)**")
        st.markdown("\n".join([f"- {x}" for x in kb.get("문화", [])]) or "- 자료 준비 중")
    with c2:
        st.markdown("**✅ 지켜야 할 예절**")
        st.markdown("\n".join([f"- {x}" for x in kb.get("지켜야할_예절", [])]) or "- 자료 준비 중")
        st.markdown("**😕 여행 시 불편한 점(주의)**")
        st.markdown("\n".join([f"- {x}" for x in kb.get("불편한점", [])]) or "- 자료 준비 중")

    with st.expander("ℹ️ 참고/한계"):
        st.write(
            """
            - 음식점/관광지 평점은 Google Places API 응답을 사용하며, 지역/시간에 따라 변동될 수 있습니다.\n
            - 네이버 지도 평점은 공식 API가 제한적이라 기본 제공하지 않습니다. 필요 시 별도 크롤링/비공식 API는 서비스 약관을 확인 후 자체 구현하세요.\n
            - 만족도 점수는 단순 가중 평균(평점×log(리뷰수)) 예시이며, 가중치/관심사/시즌 등을 반영해 조정 가능합니다.
            """
        )

else:
    st.info("나라와 도시를 선택한 뒤 ‘추천 보기’를 눌러주세요.")
```

---

## requirements.txt

```txt
streamlit>=1.36.0
pandas>=2.2.2
googlemaps>=4.10.0
python-dotenv>=1.0.1
```

---

## 사용 팁

* **Naver 평점**: 공식 Places API가 없어 기본 기능에 포함하지 않았습니다. 운영 환경 정책을 확인 후 별도 수집 로직을 플러그인처럼 추가하세요.
* **API 요금**: Google Places/Geocoding은 유료 과금 구간이 있습니다. 캐시(`@st.cache_data`)로 호출 수를 줄였습니다.
* **확장 포인트**: `COUNTRY_KB`에 나라별 문화를 계속 추가/수정하세요.
