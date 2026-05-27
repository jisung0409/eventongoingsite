import streamlit as st
import chungram_festival as chungram
import sports_festival as sports

# 앱 전체 설정
st.set_page_config(page_title="강화고등학교 행사 플랫폼", layout="wide", initial_sidebar_state="collapsed")

# 세션 상태로 현재 활성화된 페이지 관리
if 'current_page' not in st.session_state:
    st.session_state.current_page = "home"

def navigate_to(page_name):
    st.session_state.current_page = page_name
    st.rerun()

# ------------------------------------------
# 🏠 메인 홈 화면
# ------------------------------------------
if st.session_state.current_page == "home":
    st.markdown("<h1 style='text-align: center; color: #1E90FF; margin-top: -10px;'>🏫 강화고등학교 행사 통합 플랫폼</h1>", unsafe_allow_html=True)
    st.write("---")
    
    # 🔥 현재 진행 중인 행사 섹션
    st.markdown("### 🔥 현재 진행 중인 행사")
    
    # 청람학술제 바로가기 카드 레이아웃
    st.markdown("""
        <div style='background-color: #e8f4fd; padding: 20px; border-radius: 15px; border-left: 6px solid #2196F3; margin-bottom: 15px;'>
            <h2 style='margin: 0; color: #0d47a1;'>🌐 청람학술제</h2>
            <p style='margin: 10px 0 0 0; color: #1565c0; font-size: 1.1rem;'>
                현재 학술제 강연 및 발표 세션 안내가 진행 중입니다. 아래 버튼을 눌러 바로 입장하여 신청하세요!
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 청람학술제 입장하기", use_container_width=True):
        navigate_to("chungram")
        
    st.write("---")
    
    # 📁 지난 행사 섹션 (기록 보존용)
    st.markdown("### 📁 지난 행사 기록")
    col_past, _ = st.columns([1, 2])
    with col_past:
        st.markdown("""
            <div style='background-color: #f5f5f5; padding: 15px; border-radius: 12px; border-left: 5px solid #9e9e9e;'>
                <b style='color: #616161;'>🏆 2026 체육대회 (종료됨)</b><br>
                <span style='font-size: 0.9rem; color: #757575;'>최종 종합 순위 및 학년별 경기 결과를 조회할 수 있습니다.</span>
            </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("📊 체육대회 전광판 아카이브 보기", use_container_width=True):
            navigate_to("sports")

# ------------------------------------------
# 🔄 페이지 라우팅 처리
# ------------------------------------------
elif st.session_state.current_page == "chungram":
    if st.button("⬅️ 메인 화면으로 돌아가기", key="back_to_home_cr"):
        navigate_to("home")
    chungram.show_page()

elif st.session_state.current_page == "sports":
    if st.button("⬅️ 메인 화면으로 돌아가기", key="back_to_home_sp"):
        navigate_to("home")
    # 전광판 모드가 꺼진 일반 모드로 실행 (필요시 내부 락 선언 가능)
    sports.show_page()
