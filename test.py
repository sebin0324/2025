import os
import json
from typing import Dict, List, Any

import streamlit as st
import pandas as pd
import requests

# =============================
# 앱 메타 & 설정
# =============================
st.set_page_config(
    page_title="해외 여행 인사이트 · 만족도 · 추천",
    page_icon="🌍",
    layout="wide",
)

st.title("🌍 해외 여행 인사이트 · 만족도 · 추천")
st.caption("국가별 만족도, 여행지/소도시 추천, 음식 추천(구글/네이버), 불편한 점, 위생/문화 정보를 한 곳에서!")

# =============================
# 안전한 시크릿 로딩
# =============================
GOOGLE_API_KEY = None
NAVER_CLIENT_ID = None
NAVER_CLIENT_SECRET = None

try:
    GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY")
    NAVER_CLIENT_ID = st.secrets.get("NAVER_CLIENT_ID")
    NAVER_CLIENT_SECRET = st.secrets.get("NAVER_CLIENT_SECRET")
except Exception:
    # Streamlit 클라우드가 아니거나 secrets 미설정일 수 있음 - 환경변수 fallback
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
    NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")

# =============================
# 간단한 내부 데이터 (샘플)
# 실제 지표와 다를 수 있으며, 참고용 예시입니다.
# =============================
COUNTRY_PROFILES: Dict[str, Dict[str, Any]] = {
    "일본": {
        "satisfaction": 8.6,
        "cities": {
            "도쿄": ["가마쿠라", "요코하마", "하코네", "닛코"],
            "오사카": ["나라", "고베", "교토", "히메지"],
            "삿포로": ["오타루", "후라노", "비에이"]
        },
        "hygiene": [
            "공중위생 및 청결 수준이 매우 높은 편",
            "식당 위생등급 관리 잘 되어 있음",
            "수돗물 음용 가능(현지 표기 확인)"
        ],
        "culture": [
            "대중교통에서 통화 자제",
            "현금결제도 여전히 잦음",
            "가게 입구 앞 대기 줄 질서 엄수"
        ],
        "inconveniences": [
            "영어 안내가 제한적인 곳이 있음",
            "교통패스 종류가 다양해 선택이 어려울 수 있음",
            "현금 전용 가게가 가끔 있음"
        ]
    },
    "태국": {
        "satisfaction": 8.2,
        "cities": {
            "방콕": ["아유타야", "빠따야", "암파와 수상시장"],
            "치앙마이": ["치앙라이", "파이", "람푼"],
            "푸켓": ["피피섬", "팡아만", "라차섬"]
        },
        "hygiene": [
            "대부분의 관광지 식당은 위생 양호",
            "생수 구매 권장(수돗물 비음용)",
            "길거리 음식은 조리 상태 확인 후 섭취"
        ],
        "culture": [
            "사원 방문 시 노출이 심한 복장 지양",
            "왕실 관련 언행 주의",
            "쓰레기 무단 투기 금지, 흡연 구역 확인"
        ],
        "inconveniences": [
            "더위와 습도에 따른 피로감",
            "교통체증 심한 시간대 존재",
            "택시/툭툭 흥정 필요할 수 있음"
        ]
    },
    "프랑스": {
        "satisfaction": 8.0,
        "cities": {
            "파리": ["베르사유", "지베르니", "퐁텐블로"],
            "니스": ["칸", "앙티브", "에즈"],
            "리옹": ["베죵스", "안시", "페루즈"]
        },
        "hygiene": [
            "대도시 공공장소는 평균적 위생",
            "식당/빵집 품질 관리 엄격",
            "수돗물 대체로 음용 가능"
        ],
        "culture": [
            "인사(봉쥬르)와 기본 예의 중요",
            "식당 팁은 선택이나 서비스 포함 여부 확인",
            "박물관/성당 내 소란 금지"
        ],
        "inconveniences": [
            "소매치기 주의(특히 관광지)",
            "영업시간 제한(일요일 휴무 다수)",
            "대중시위로 특정 일시 교통 불편 가능"
        ]
    },
    "미국": {
        "satisfaction": 8.1,
        "cities": {
            "뉴욕": ["브루클린", "저지시티", "롱아일랜드 시티"],
            "LA": ["산타모니카", "말리부", "패사디나"],
            "샌프란시스코": ["소살리토", "버클리", "오클랜드"]
        },
        "hygiene": [
            "지역별 편차 큼",
            "수돗물 음용 가능 지역 다수(현지 확인)",
            "자동차 이동 중심 인프라"
        ],
        "culture": [
            "팁 문화(식당 15~20% 일반적)",
            "대화 시 개인 공간 존중",
            "흡연/음주 규정 준수"
        ],
        "inconveniences": [
            "대중교통 빈도 낮은 지역 존재",
            "도시 치안 구역 확인 필요",
            "가격/세금/팁으로 체감물가 상승"
        ]
    },
    "베트남": {
        "satisfaction": 8.3,
        "cities": {
            "하노이": ["닌빈", "하롱베이", "박닌"],
            "호치민": ["꾸찌터널", "빈롱", "브이웅따우"],
            "다낭": ["호이안", "바나힐", "후에"]
        },
        "hygiene": [
            "관광지 식당은 대체로 양호",
            "생수 권장(수돗물 비음용)",
            "길거리 음식은 조리/보관 상태 확인"
        ],
        "culture": [
            "오토바이 교통량 많아 보행 시 주의",
            "현지 시장 흥정 문화",
            "사원/사당 방문 시 복장 유의"
        ],
        "inconveniences": [
            "교통 소음/매연",
            "습한 기후와 갑작스런 소나기",
            "카드 결제 안되는 상점 존재"
        ]
    },
}

# 기본 국가 목록(UI에서 보여줄 옵션)
COUNTRY_OPTIONS = list(COUNTRY_PROFILES.keys())

# =============================
# 유틸: API 호출 캐시
# =============================
@st.cache_data(show_spinner=False)
def google_text_search(query: str, api_key: str, language: str = "ko") -> Dict[str, Any]:
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {"query": query, "key": api_key, "language": language}
    try:
        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}

@st.cache_data(show_spinner=False)
def naver_local_search(query: str, client_id: str, client_secret: str) -> Dict[str, Any]:
    # Naver Local Search API (문서: https://developers.naver.com/docs/serviceapi/search/local/local.md)
    # 최대 5개 정도만 가져오고 정렬은 기본 정확도
    url = "https://openapi.naver.com/v1/search/local.json"
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret,
    }
    params = {"query": query, "display": 5}
    try:
        r = requests.get(url, headers=headers, params=params, timeout=15)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}

# =============================
# 음식점 추천 로직
# =============================
def fetch_top_restaurants(country: str, city: str, topn: int = 3) -> List[Dict[str, Any]]:
    """가능하면 NAVER → GOOGLE 순서로 시도. 둘 다 없으면 샘플 데이터 반환."""
    results: List[Dict[str, Any]] = []

    # 1) NAVER
    if NAVER_CLIENT_ID and NAVER_CLIENT_SECRET:
        q = f"{country} {city} 맛집"
        data = naver_local_search(q, NAVER_CLIENT_ID, NAVER_CLIENT_SECRET)
        items = data.get("items", []) if isinstance(data, dict) else []
        for it in items[:topn]:
            # Naver는 좌표 제공 X (Local 검색은 기본 데이터만), 지도 링크/전화/주소 위주
            results.append({
                "name": it.get("title", "").replace("<b>", "").replace("</b>", ""),
                "address": it.get("roadAddress") or it.get("address"),
                "link": it.get("link"),
                "category": it.get("category"),
                "tel": it.get("telephone"),
                "source": "Naver",
                "lat": None,
                "lon": None,
                "rating": None,
            })
        if results:
            return results[:topn]

    # 2) GOOGLE
    if GOOGLE_API_KEY:
        q = f"best restaurants in {city} {country}"
        data = google_text_search(q, GOOGLE_API_KEY, language="ko")
        candidates = data.get("results", []) if isinstance(data, dict) else []
        # 평점과 리뷰 수 기준으로 상위 정렬
        def sort_key(x):
            return (x.get("rating", 0), x.get("user_ratings_total", 0))
        candidates.sort(key=sort_key, reverse=True)
        for c in candidates[:topn]:
            loc = c.get("geometry", {}).get("location", {})
            results.append({
                "name": c.get("name"),
                "address": c.get("formatted_address"),
                "link": f"https://www.google.com/maps/place/?q=place_id:{c.get('place_id')}",
                "category": ", ".join(c.get("types", [])[:3]) if c.get("types") else None,
                "tel": None,
                "source": "Google",
                "lat": loc.get("lat"),
                "lon": loc.get("lng"),
                "rating": c.get("rating"),
            })
        if results:
            return results[:topn]

    # 3) Fallback 샘플
    sample = [
        {"name": "Sample Bistro", "address": f"{city} 중심가", "link": None, "category": "Bistro", "tel": None, "source": "Sample", "lat": None, "lon": None, "rating": 4.5},
        {"name": "Local Eats", "address": f"{city} 인기 거리", "link": None, "category": "Local", "tel": None, "source": "Sample", "lat": None, "lon": None, "rating": 4.4},
        {"name": "Top Grill", "address": f"{city} 유명 스팟", "link": None, "category": "Grill", "tel": None, "source": "Sample", "lat": None, "lon": None, "rating": 4.3},
    ]
    return sample[:topn]

# =============================
# 사이드바
# =============================
st.sidebar.header("⚙️ 설정")
country = st.sidebar.selectbox("국가를 선택하세요", COUNTRY_OPTIONS, index=0)
city_options = list(COUNTRY_PROFILES[country]["cities"].keys())
city = st.sidebar.selectbox("주요 도시 선택", city_options, index=0)

st.sidebar.info(
    "음식점 추천은 NAVER/GOOGLE API 키가 있을 때 자동으로 상위 평점 장소 3곳을 보여줍니다.\n"
    "키가 없으면 샘플 데이터를 보여줘요."
)

# =============================
# 상단 KPI: 만족도 & 요약
# =============================
profile = COUNTRY_PROFILES.get(country, {})
satisfaction = profile.get("satisfaction")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("여행자 만족도(샘플)", f"{satisfaction:.1f} / 10")
with col2:
    st.metric("추천 주요 도시 수", len(profile.get("cities", {})))
with col3:
    st.metric("도시 내 소도시/근교 추천 수", sum(len(v) for v in profile.get("cities", {}).values()))

st.divider()

# =============================
# 섹션 1) 도시 & 소도시/근교 추천
# =============================
st.subheader("🏙️ 여행지 추천")

city_tabs = st.tabs([*profile["cities"].keys()])
for idx, (main_city, daytrips) in enumerate(profile["cities"].items()):
    with city_tabs[idx]:
        st.markdown(f"**주요 도시:** {main_city}")
        if daytrips:
            st.markdown("**소도시/근교 추천:** ")
            chips = ", ".join(daytrips)
            st.write(chips)
        else:
            st.write("소도시 데이터가 없습니다.")

st.divider()

# =============================
# 섹션 2) 음식 추천(실시간 API)
# =============================
st.subheader("🍽️ 음식 추천 (상위 평점 3곳)")
with st.spinner("최고 평점 맛집을 찾는 중..."):
    restaurants = fetch_top_restaurants(country, city, topn=3)

if restaurants:
    df = pd.DataFrame(restaurants)
    # 지도 표시 가능한 데이터만 분리
    mappable = df.dropna(subset=["lat", "lon"]) if {"lat", "lon"}.issubset(df.columns) else pd.DataFrame()

    for i, row in df.iterrows():
        left, right = st.columns([2, 3])
        with left:
            st.markdown(f"### {row['name']}")
            meta = []
            if pd.notna(row.get("rating")):
                meta.append(f"⭐ {row['rating']}")
            if row.get("category"):
                meta.append(f"{row['category']}")
            if meta:
                st.caption(" · ".join(meta))
            if row.get("address"):
                st.write(row["address"])
            if row.get("tel"):
                st.write(f"전화: {row['tel']}")
            if row.get("link"):
                st.link_button("상세 보기", row["link"], use_container_width=True)
            st.caption(f"출처: {row.get('source', 'N/A')}")
        with right:
            if pd.notna(row.get("lat")) and pd.notna(row.get("lon")):
                map_df = pd.DataFrame({"lat": [row["lat"]], "lon": [row["lon"]]})
                st.map(map_df, use_container_width=True, zoom=13)
            else:
                st.info("지도를 표시하려면 Google Places 결과가 필요합니다.")
else:
    st.warning("음식점 데이터를 찾지 못했습니다.")

st.divider()

# =============================
# 섹션 3) 위생, 문화, 불편한 점
# =============================
st.subheader("🧼 위생 · 🧭 문화 · ⚠️ 불편한 점")

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("#### 🧼 위생")
    for item in profile.get("hygiene", []):
        st.write("• ", item)

with c2:
    st.markdown("#### 🧭 지켜야 하는 문화/매너")
    for item in profile.get("culture", []):
        st.write("• ", item)

with c3:
    st.markdown("#### ⚠️ 불편할 수 있는 점")
    for item in profile.get("inconveniences", []):
        st.write("• ", item)

st.divider()

# =============================
# 참고 / 고지
# =============================
with st.expander("ℹ️ 참고 및 고지사항"):
    st.markdown(
        """
        - 본 앱의 만족도 수치와 도시/소도시 추천은 **샘플 데이터**이며, 최신 통계와 다를 수 있어요.
        - 음식점 추천은 **Naver Local Search API** 또는 **Google Places API**를 사용해 상위 평점 장소를 가져옵니다(가능한 경우).
        - API 키가 없거나 호출에 실패하면 샘플 데이터가 표시됩니다.
        - 여행 계획 시 공식 관광 사이트/최신 리뷰를 함께 확인하세요.
        """
    )

# =============================
# 사이드 도움말: API 설정 안내
# =============================
with st.sidebar.expander("🗝️ API 키 설정 방법"):
    st.markdown(
        """
        **Streamlit Cloud**에서 `⚙️ Settings → Secrets`에 아래 키를 추가:

        ```toml
        GOOGLE_API_KEY = "..."
        NAVER_CLIENT_ID = "..."
        NAVER_CLIENT_SECRET = "..."
        ```

        **로컬 실행** 시에는 터미널에서 환경변수로 지정하거나, 프로젝트 루트에 `.streamlit/secrets.toml` 파일을 만들어 동일 키를 넣으세요.
        """
    )

st.success("✅ 설정/데이터 입력 후 상단에서 국가와 도시를 선택해보세요!")
