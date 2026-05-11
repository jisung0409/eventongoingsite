import streamlit as st
import sports_festival 
import academic_fest

# 1. 웹앱 기본 설정
st.set_page_config(
    page_title="강화고 행사 통합 관리 시스템", 
    page_icon="🏫", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# [핵심] 학교스럽고 밝은 느낌을 꽉 채워주는 커스텀 CSS
st.markdown("""
<style>
/* 전체 화면 배경: 맑은 하늘색과 연보라색 그라데이션으로 빈 공간 채우기 */
.stApp {
    background: linear-gradient(120deg, #e0c3fc 0%, #8ec5fc 100%);
}

/* 메인 컨텐츠 영역: 모서리가 둥근 거대한 흰색 카드로 만들어 깔끔하게 정리 */
.main .block-container {
    background-color: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    padding: 2rem;
    margin-top: 2rem;
    margin-bottom: 2rem;
    box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.1);
}

/* 사이드바 배경도 밝고 투명하게 */
[data-testid="stSidebar"] {
    background-color: rgba(255, 255, 255, 0.7);
}

/* 버튼 디자인: 둥글고 눈에 띄게 */
.stButton>button {
    border-radius: 20px;
    border: 2px solid #8ec5fc;
    color: #333;
    font-weight: bold;
    background-color: #ffffff;
    transition: 0.3s;
}
.stButton>button:hover {
    background-color: #8ec5fc;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# 2. 사이드바 네비게이션
with st.sidebar:
    st.header("📌 강화고 행사 메뉴")
    menu = st.radio(
        "이동할 페이지를 선택하세요:",
        [
            "🏠 홈", 
            "🏆 체육대회",
            "📚 청람 학술제",
            "🎪 마리마당 축제", 
            "💡 행사 추천 및 설문"
        ]
    )
    st.divider()
    st.caption("👨‍💻 개발팀: 헬로월드 (코딩동아리)")
    st.caption("👨‍💻 개발자: 30508 김지성")

# 3. 페이지 라우팅
if menu == "🏠 홈":
    st.title("🏫 강화고 행사 톡톡!")
    st.markdown("### 우리 학교의 모든 행사를 한곳에서! 🎉")
    st.info("👈 왼쪽 메뉴에서 원하는 행사를 탭해 보세요.")
    
    st.divider()
    st.subheader("🔥 현재 진행 중인 행사")
    st.success("⚽ **[진행 중]** 2026 강화고 체육대회 (메뉴에서 확인!)")

elif menu == "🏆 체육대회":
    sports_festival.show_page()

elif menu == "🎪 마리마당 축제":
    st.title("🎪 마리마당 축제")
    st.write("알록달록한 마리마당 축제 전용 페이지가 들어갈 자리입니다.")

elif menu == "📚 청람 학술제":
    academic_fest.show_page()

elif menu == "💡 행사 추천 및 설문":
    st.title("💡 행사 추천 및 설문조사")
    st.write("학생들의 의견을 수집하고 설문조사를 진행하는 공간입니다.")
