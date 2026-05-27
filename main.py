import streamlit as st
import chungram_festival as chungram
import sports_festival as sports

# 앱 전체 설정
st.set_page_config(page_title="강화고 행사 플랫폼", layout="wide", initial_sidebar_state="collapsed")

# ==========================================
# 🎨 UI/UX 꾸미기 (커스텀 CSS 주입)
# ==========================================
# CSS 텍스트도 왼쪽으로 쫙 붙여서 버그를 원천 차단합니다.
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
header { visibility: hidden; }

.event-card {
    background-color: #ffffff; padding: 25px; border-radius: 15px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border-left: 8px solid #2196F3; margin-bottom: 15px;
}
.event-card:hover {
    transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.15);
}

.archive-card {
    background-color: #ffffff; padding: 20px; border-radius: 12px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05); transition: transform 0.2s ease;
    border-left: 6px solid #9ca3af; opacity: 0.9; margin-bottom: 15px;
}
.archive-card:hover { transform: translateY(-3px); opacity: 1; }

.calendar-box {
    background-color: #ffffff; padding: 20px 25px; border-radius: 15px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    border-left: 8px solid #10B981; height: 400px; overflow-y: auto;
}
.cal-month {
    color: #047857; font-size: 1.15rem; font-weight: 800;
    margin-top: 20px; margin-bottom: 8px;
    border-bottom: 2px solid #ecfdf5; padding-bottom: 5px;
}
.cal-month:first-child { margin-top: 0; }
.cal-item {
    color: #4b5563; font-size: 0.95rem; margin-bottom: 6px;
    line-height: 1.5; padding-left: 10px; text-indent: -10px;
}

.calendar-box::-webkit-scrollbar { width: 8px; }
.calendar-box::-webkit-scrollbar-track { background: #f1f1f1; border-radius: 10px; }
.calendar-box::-webkit-scrollbar-thumb { background: #d1d5db; border-radius: 10px; }
.calendar-box::-webkit-scrollbar-thumb:hover { background: #9ca3af; }
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
    
    if st.button("🚀 청람학술제 바로 입장하기", use_container_width=True, type="primary"):
        navigate_to("chungram")
        
    st.markdown("<br><hr style='border: 1px solid #D1D5DB; margin: 20px 0 30px 0;'>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns([1, 1.2])
    
    with col_left:
        st.markdown("<h3 style='color: #4B5563; margin-bottom: 15px;'>📁 지난 행사 기록</h3>", unsafe_allow_html=True)
        
        st.markdown("""
<div class="archive-card">
    <b style='color: #374151; font-size: 1.1rem;'>🏆 2026 체육대회 (종료)</b><br>
    <div style='font-size: 0.9rem; color: #6B7280; line-height: 1.5; margin-top: 5px;'>
        열정 넘쳤던 학년별 경기 결과와 최종 종합 순위를 다시 열람할 수 있습니다.
    </div>
</div>
        """, unsafe_allow_html=True)
        
        if st.button("📊 체육대회 전광판 아카이브", use_container_width=True):
            navigate_to("sports")
            
        st.write("")
        
        st.markdown("""
<div class="archive-card" style="border-left: 6px solid #e5e7eb; background-color: #f9fafb; display: flex; align-items: center; justify-content: center; height: 110px;">
    <div style="text-align: center; color: #9ca3af; font-size: 1rem; font-weight: 600;">
        🔜 다음 행사를 준비 중입니다
    </div>
</div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown("<h3 style='color: #047857; margin-bottom: 15px;'>📅 2026~2027 학사일정</h3>", unsafe_allow_html=True)
        
        # 👇 이 부분이 핵심! 띄어쓰기를 전부 없애서 왼쪽 벽에 밀착시켰습니다.
        st.markdown("""
<div class="calendar-box">
    <div class="cal-month">2026년 6월</div>
    <div class="cal-item"><b>03일:</b> 지방선거</div>
