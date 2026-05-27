import streamlit as st
import chungram_festival as chungram
import sports_festival as sports

# 앱 전체 설정
st.set_page_config(page_title="강화고 행사 플랫폼", layout="wide", initial_sidebar_state="collapsed")

# ==========================================
# 🎨 UI/UX 꾸미기 (커스텀 CSS 주입)
# ==========================================
st.markdown("""
    <style>
        /* 1. 전체 배경 부드러운 그라데이션 적용 */
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }
        
        /* 2. 스트림릿 기본 상단 바 숨기기 (더 앱처럼 보이게) */
        header {visibility: hidden;}
        
        /* 3. 진행 중인 행사 카드 디자인 & 마우스 호버 애니메이션 */
        .event-card {
            background-color: #ffffff;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border-left: 8px solid #2196F3;
            margin-bottom: 15px;
        }
        .event-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.15);
        }
        
        /* 4. 종료된 행사(아카이브) 카드 디자인 */
        .archive-card {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            transition: transform 0.2s ease;
            border-left: 6px solid #9e9e9e;
            opacity: 0.85; /* 살짝 투명하게 해서 지나간 느낌 주기 */
        }
        .archive-card:hover {
            transform: translateY(-3px);
            opacity: 1;
        }
    </style>
""", unsafe_allow_html=True)

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
    st.write("<br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #1E3A8A; font-weight: 800; font-size: 3rem;'>🏫 강화고등학교 통합 플랫폼</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #4B5563; font-size: 1.2rem; margin-bottom: 40px;'>우리 학교의 모든 행사와 일정을 한곳에서 확인하세요.</p>", unsafe_allow_html=True)
    
    # 레이아웃을 중앙으로 예쁘게 모아주기 위한 빈 컬럼 트릭
    _, col_main, _ = st.columns([1, 8, 1])
    
    with col_main:
        # 🔥 현재 진행 중인 행사 섹션
        st.markdown("<h3 style='color: #111827; margin-bottom: 15px;'>🔥 현재 진행 중인 행사</h3>", unsafe_allow_html=True)
        
        st.markdown("""
            <div class="event-card">
                <h2 style='margin: 0; color: #1E40AF;'>🌐 제1회 청람학술제</h2>
                <p style='margin: 10px 0 5px 0; color: #3B82F6; font-size: 1.15rem; font-weight: 600;'>
                    현재 강연 및 발표 세션 안내와 가신청이 진행 중입니다.
                </p>
                <p style='margin: 0; color: #6B7280; font-size: 0.95rem;'>
                    👉 진로와 관심사에 맞는 세션을 둘러보고 늦지 않게 신청서를 제출해 주세요!
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # 버튼 포인트 컬러 주기 (type="primary")
        if st.button("🚀 청람학술제 바로 입장하기", use_container_width=True, type="primary"):
            navigate_to("chungram")
            
        st.markdown("<br><hr style='border: 1px solid #D1D5DB; margin: 30px 0;'><br>", unsafe_allow_html=True)
        
        # 📁 지난 행사 섹션
        st.markdown("<h3 style='color: #4B5563; margin-bottom: 15px;'>📁 지난 행사 기록</h3>", unsafe_allow_html=True)
        col_past, _ = st.columns([1, 1.5])
        
        with col_past:
            st.markdown("""
                <div class="archive-card">
                    <b style='color: #374151; font-size: 1.1rem;'>🏆 2026 체육대회 (종료)</b><br>
                    <span style='font-size: 0.9rem; color: #6B7280; line-height: 1.6;'>
                        열정 넘쳤던 학년별 경기 결과와<br>최종 종합 순위를 다시 열람할 수 있습니다.
                    </span>
                </div>
            """, unsafe_allow_html=True)
            st.write("")
            if st.button("📊 체육대회 전광판 아카이브", use_container_width=True):
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
    sports.show_page()
