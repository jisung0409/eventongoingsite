import streamlit as st
import sports_festival # 방금 만든 체육대회 파일
# import marimadang # 나중에 연결할 파일
# import academic_fest # 나중에 연결할 파일

# 1. 웹앱 기본 설정 (다크모드 감성에 맞게 아이콘과 제목 설정)
st.set_page_config(
    page_title="강화고 행사 통합 관리 시스템", 
    page_icon="⚡", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# 2. 사이드바 네비게이션
with st.sidebar:
    st.header("📌 강화고 행사 메뉴")
    menu = st.radio(
        "이동할 페이지를 선택하세요:",
        [
            "🏠 홈", 
            "🏆 체육대회", 
            "🎪 마리마당 축제", 
            "📚 청람 학술제", 
            "💡 행사 추천 및 설문"
        ]
    )
    st.divider()
    # 개발자 정보
    st.caption("👨‍💻 개발팀: 헬로월드 (코딩동아리)")
    st.caption("👨‍💻 개발자: 30508 김지성")
    st.caption("⚙️ 시스템 버전: v1.0")

# 3. 페이지 라우팅 (선택한 메뉴에 따라 화면 변경)
if menu == "🏠 홈":
    st.title("⚡ 강화고 행사 통합 관리 시스템")
    st.markdown("### 환영합니다! 강화고등학교의 모든 행사를 한곳에서 확인하세요.")
    st.info("👈 왼쪽 사이드바에서 원하는 행사를 선택해 주세요.")
    
    st.divider()
    # 홈 화면에 현재 진행 중인 행사 하이라이트
    st.subheader("🔥 현재 진행 중인 행사")
    st.success("**[진행 중]** 2026 강화고 e-체육대회 (상단 메뉴에서 확인하세요!)")

elif menu == "🏆 체육대회":
    # 분리해둔 체육대회 페이지 화면 불러오기
    sports_festival.show_page()

elif menu == "🎪 마리마당 축제":
    st.title("🎪 마리마당 축제")
    st.write("알록달록한 마리마당 축제 전용 페이지가 들어갈 자리입니다.")
    # marimadang.show_page() # 나중에 이 주석을 풀고 연결합니다.

elif menu == "📚 청람 학술제":
    st.title("📚 청람 학술제")
    st.write("지적이고 차분한 학술제 전용 페이지가 들어갈 자리입니다.")
    # academic_fest.show_page() # 나중에 이 주석을 풀고 연결합니다.

elif menu == "💡 행사 추천 및 설문":
    st.title("💡 행사 추천 및 설문조사")
    st.write("학생들의 의견을 수집하고 설문조사를 진행하는 공간입니다.")
