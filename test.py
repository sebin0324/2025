# app.py
import streamlit as st
import pandas as pd
import requests
from urllib.parse import quote

# ---------------------------
# 페이지/시크릿 설정
# ---------------------------
st.set_page_config(page_title="해외여행 추천(실시간 맛집)", page_icon="🌍", layout="wide")

GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY", None)          # Google Places API (Text Search)
NAVER_CLIENT_ID = st.secrets.get("NAVER_CLIENT_ID", None)        # Naver Local Search
NAVER_CLIENT_SECRET = st.secrets.get("NAVER_CLIENT_SECRET", None)

# ---------------------------
# 한국인 인기 여행지 샘플 데이터
# ---------------------------
COUNTRY_DATA = {
    "일본": {
        "만족도": 4.7,
        "도시": {
            "도쿄": ["요코하마", "가마쿠라", "하코네"],
            "오사카": ["교토", "나라", "고베"],
            "후쿠오카": ["다자이후", "이토시마", "야나가와"],
        },
        "위생": ["수돗물 대체로 안전", "길거리 음식 위생 양호", "쓰레기 분리 철저"],
        "문화": ["질서·조용함 중시", "줄서기/새치기 금지", "온천 문신 규정 확인"],
        "불편": ["영어 소통 난이도", "교통비 부담", "현금-only 가게 일부"],
        "대표음식키워드": "스시 라멘 오코노미야키",
    },
    "태국": {
        "만족도": 4.4,
        "도시": {
            "방콕": ["아유타야", "파타야", "깐짜나부리"],
            "푸켓": ["피피섬", "카오락", "팡아"],
            "치앙마이": ["치앙라이", "매홍손", "람푼"],
        },
        "위생": ["생수 마시기 권장", "얼음/생야채 주의", "손소독제 지참"],
        "문화": ["왕실 존중 필수", "사원 복장 규정", "발가락·머리 터치 금기"],
        "불편": ["고온다습 기후", "교통혼잡", "바가지/호객"],
        "대표음식키워드": "팟타이 똠얌꿍 망고스티키라이스",
    },
    "베트남": {
        "만족도": 4.5,
        "도시": {
            "하노이": ["하롱베이", "닌빈", "사파"],
            "호치민": ["메콩델타", "붕따우", "꾸찌터널"],
            "다낭": ["호이안", "바나힐", "후에"],
        },
        "위생": ["생수 권장", "얼음/샐러드 주의", "길거리 음식 신뢰도 확인"],
        "문화": ["가격 흥정 문화", "오토바이 교통 주의", "현지 통화 소액권 유용"],
        "불편": ["오토바이 소음/매연", "스콜성 비", "QR/카드 결제 편차"],
        "대표음식키워드": "쌀국수 반미 분짜",
    },
    "미국": {
        "만족도": 4.3,
        "도시": {
            "뉴욕": ["저지시티", "필라델피아", "보스턴"],
            "로스앤젤레스": ["샌디에이고", "라스베가스", "샌타바버라"],
            "하와이(호놀룰루)": ["오아후 섬일주", "카일루아", "북쇼어"],
        },
        "위생": ["수돗물 지역차 존재", "레스토랑 위생 등급 표기", "팁 문화로 서비스 유지"],
        "문화": ["팁(15~20%) 관례", "개인 공간 존중", "신분증 소지(주류·클럽)"],
        "불편": ["물가/세금·팁 부담", "총기 관련 안전 이슈", "도심 주차난"],
        "대표음식키워드": "버거 스테이크 타코",
    },
    "프랑스": {
        "만족도": 4.5,
        "도시": {
            "파리": ["베르사유", "지베르니", "몽생미셸(장거리)"],
            "니스": ["칸", "앙티브", "모나코"],
            "리옹": ["안시", "그르노블", "디종"],
        },
        "위생": ["수돗물 대체로 안전", "생치즈/생고기 주의", "레스토랑 위생 준수"],
        "문화": ["간단한 불어 인사 예의", "식사시간/시에스타", "드레스코드 신경"],
        "불편": ["소매치기 주의", "파업/집회 변동성", "일요일 영업 제한"],
        "대표음식키워드": "크루아상 스테이크타르타르 와인",
    },
    "스페인": {
        "만족도": 4.5,
        "도시": {
            "바르셀로나": ["시체스", "타라고나", "히로나"],
            "마드리드": ["똘레도", "세고비아", "아비라"],
            "세비야": ["코르도바", "그라나다", "카디스"],
        },
        "위생": ["수돗물 지역차", "타파스 위생 양호", "늦은 식사 문화"],
        "문화": ["시에스타(점심후 휴무)", "저녁식사 늦게", "소매치기 주의"],
        "불편": ["언어 장벽(영·스)", "영업시간 변동", "관광지 혼잡"],
        "대표음식키워드": "파에야 하몽 타파스",
    },
    "싱가포르": {
        "만족도": 4.6,
        "도시": {
            "싱가포르": ["리틀인디아", "차이나타운", "티옹바루"],
        },
        "위생": ["수돗물 안전", "호커센터 위생 관리 양호", "실내냉방 강함"],
        "문화": ["깨끗함 유지(벌금 엄격)", "줄서기/공공질서 준수", "껌 반입 금지"],
        "불편": ["물가 비쌈", "실내외 온도차", "술값 비쌈"],
        "대표음식키워드": "치킨라이스 락사 칠리크랩",
    },
}

# ---------------------------
# API 호출 함수들 (캐시)
# ---------------------------
@st.cache_data(show_spinner=False, ttl=3600)
def google_places_text_search(query: str, language: str = "ko", limit: int = 3):
    """Google Places Text Search: 평점/리뷰수 포함"""
    if not GOOGLE_API_KEY:
        return [], "Google API Key 없음"
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {"query": query, "key": GOOGLE_API_KEY, "language": language}
    try:
        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        items = r.json().get("results", [])
        items = sorted(
            items,
            key=lambda x: (x.get("rating", 0), x.get("user_ratings_total", 0)),
            reverse=True,
        )[:limit]
        results = []
        for it in items:
            name = it.get("name")
            rating = it.get("rating")
            reviews = it.get("user_ratings_total")
            address = it.get("formatted_address", "")
            place_id = it.get("place_id")
            link = f"https://www.google.com/maps/search/?api=1&query={quote(name)}&query_place_id={place_id}" if place_id else None
            results.append(
                {
                    "source": "Google",
                    "name": name,
                    "rating": rating,
                    "reviews": reviews,
                    "address": address,
                    "link": link,
                }
            )
        return results, None
    except Exception as e:
        return [], f"Google API 오류: {e}"

@st.cache_data(show_spinner=False, ttl=3600)
def naver_local_search(query: str, display: int = 3):
    """Naver Local Search: 평점 미제공(상호/주소/링크만)"""
    if not (NAVER_CLIENT_ID and NAVER_CLIENT_SECRET):
        return [], "Naver API Key 없음"
    url = "https://openapi.naver.com/v1/search/local.json"
    params = {"query": query, "display": display, "start": 1, "sort": "comment"}
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
    }
    try:
        r = requests.get(url, params=params, headers=headers, timeout=15)
        r.raise_for_status()
        items = r.json().get("items", [])
        results = []
        for it in items[:display]:
            title = it.get("title", "").replace("<b>", "").replace("</b>", "")
            address = it.get("roadAddress") or it.get("address") or ""
            link = it.get("link") or None
            results.append(
                {
                    "source": "Naver",
                    "name": title,
                    "rating": None,
                    "reviews": None,
                    "address": address,
                    "link": link,
                }
            )
        return results, None
    except Exception as e:
        return [], f"Naver API 오류: {e}"

def search_restaurants(city: str, keyword: str, use_google: bool, use_naver: bool, limit: int = 3):
    results, errors = [], []
    query = f"{city} {keyword}".strip()

    if use_google:
        g, err = google_places_text_search(query, language="ko", limit=limit)
        results.extend(g)
        if err: errors.append(err)

    if use_naver:
        n, err = naver_local_search(query, display=limit)
        results.extend(n)
        if err: errors.append(err)

    return results, errors

# ---------------------------
# UI
# ---------------------------
st.title("🌍 해외여행 만족도 & 추천 가이드 (실시간 맛집 포함)")
st.caption("한국인 인기 여행지를 중심으로, 만족도/도시·소도시/위생·문화/불편한 점과 실시간 맛집 정보를 제공합니다.")

left, right = st.columns([1, 2], gap="large")

with left:
    country = st.selectbox("나라 선택", list(COUNTRY_DATA.keys()))
    city = None
    if country:
        cities = list(COUNTRY_DATA[country]["도시"].keys())
        city = st.selectbox("도시 선택", cities)
        small_cities = COUNTRY_DATA[country]["도시"].get(city, [])

    st.divider()
    st.markdown("**맛집 검색 옵션**")
    default_kw = COUNTRY_DATA[country]["대표음식키워드"] if country else "맛집"
    keyword = st.text_input("검색 키워드(예: 스시, 파에야, 버거…)", value=default_kw)
    source = st.multiselect(
        "데이터 소스 선택",
        ["Google(평점)", "Naver(링크)"],
        default=["Google(평점)", "Naver(링크)"],
    )
    limit = st.slider("맛집 표시 개수(소스별)", min_value=1, max_value=5, value=3, step=1)

with right:
    if country:
        data = COUNTRY_DATA[country]
        st.subheader(f"🇺🇳 {country} 여행 인포")

        mc1, mc2, mc3 = st.columns(3)
        mc1.metric("여행 만족도(5점)", f"{data['만족도']}")
        mc2.metric("추천 도시 수", f"{len(data['도시'])}")
        mc3.metric("소도시(예시)", f"{len([s for v in data['도시'].values() for s in v])}")

        st.markdown("### 📍 추천 도시 → 소도시")
        for c, subs in data["도시"].items():
            st.write(f"- **{c}** → {', '.join(subs)}")

        st.markdown("### 🧼 위생 팁")
        st.write("• " + " / ".join(data["위생"]))

        st.markdown("### 🧭 꼭 지켜야 하는 문화/알아둘 점")
        st.write("• " + " / ".join(data["문화"]))

        st.markdown("### ⚠️ 불편한 점")
        st.write("• " + " / ".join(data["불편"]))

        st.markdown("### 📊 나라별 만족도 비교")
        df = pd.DataFrame(
            {"나라": list(COUNTRY_DATA.keys()),
             "만족도": [COUNTRY_DATA[c]["만족도"] for c in COUNTRY_DATA]}
        ).set_index("나라")
        st.bar_chart(df)

        st.divider()
        st.markdown("### 🍽️ 실시간 맛집 추천")
        if not city:
            st.info("도시를 선택하면 맛집을 검색합니다.")
        else:
            use_google = "Google(평점)" in source
            use_naver = "Naver(링크)" in source

            if not use_google and not use_naver:
                st.warning("최소 1개 이상의 소스를 선택하세요.")
            else:
                if use_google and not GOOGLE_API_KEY:
                    st.warning("🔑 Google API 키가 설정되지 않았습니다. secrets.toml에 GOOGLE_API_KEY를 추가하세요.")
                if use_naver and not (NAVER_CLIENT_ID and NAVER_CLIENT_SECRET):
                    st.warning("🔑 Naver API 키가 설정되지 않았습니다. secrets.toml에 NAVER_CLIENT_ID/SECRET을 추가하세요.")

                with st.spinner(f"‘{city}’ 맛집 검색 중..."):
                    results, errs = search_restaurants(city, keyword, use_google, use_naver, limit)

                for e in errs:
                    st.error(e)

                if results:
                    table = pd.DataFrame(results)
                    sort_cols = [c for c in ["rating", "reviews"] if c in table.columns]
                    if sort_cols:
                        table = table.sort_values(by=sort_cols, ascending=False)
                    show_cols = [c for c in ["source", "name", "rating", "reviews", "address", "link"] if c in table.columns]
                    st.dataframe(table[show_cols], use_container_width=True)
                else:
                    st.info("검색 결과가 없습니다. 키워드를 바꾸거나 소스를 변경해보세요.")

