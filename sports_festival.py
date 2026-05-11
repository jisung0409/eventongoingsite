import streamlit as st
import datetime

def show_page():
    # 1. 다크모드 감성의 헤더 및 선생님 한마디 (모듈화 변수)
    st.markdown("<h1 style='text-align: center; color: #00FFCC;'>⚡ 2026 강화고 e-체육대회 ⚡</h1>", unsafe_allow_html=True)
    
    # 기선쌤의 한마디 (나중에 DB나 변수에서 불러오기 쉽게 분리)
    teacher_quote = "다치지 말고 체육대회 모두 파이팅~ 👊"
    st.info(f"📢 **기선쌤의 한마디:** {teacher_quote}")
    st.divider()

    # 2. 행사 진행 상태 표시 (종료 시 문구 변경 로직)
    today = datetime.date.today()
    event_end_date = datetime.date(2026, 5, 20) # 체육대회 종료일 설정
    
    if today > event_end_date:
        st.error("🏆 올해 체육대회가 모두 종료되었습니다. 내년을 기약해 주세요! ㅠㅠ")
    else:
        st.success("🔥 현재 체육대회가 뜨겁게 진행 중입니다! 🔥")

    # 3. 직관적인 공지사항 및 일정 (아코디언 메뉴로 깔끔하게)
    st.markdown("### 🗓️ 오늘의 매치업")
    with st.expander("👉 종목별 결승전 시간표 보기", expanded=True):
        st.write("⚽ **축구 결승:** 3학년 5반 vs 3학년 8반 (14:00 @대운동장)")
        st.write("🏀 **농구 결승:** 2학년 1반 vs 2학년 4반 (15:30 @실내체육관)")
        st.write("🏃 **계주 결승:** 전 학년 통합 (16:30 @대운동장 트랙)")

    st.divider()

    # 4. 남고 승부욕 자극: 명예의 전당 (게임 티어 시스템 차용)
    st.markdown("### 👑 명예의 전당 (Hall of Fame)")
    st.caption("실시간 종목별 종합 우승 현황입니다.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<h3 style='text-align: center; color: #FFD700;'>🥇 챌린저 (1위)</h3>", unsafe_allow_html=True)
        st.success("**3학년 5반** (축구 우승, 계주 2위)")
        
    with col2:
        st.markdown("<h3 style='text-align: center; color: #C0C0C0;'>🥈 그랜드마스터 (2위)</h3>", unsafe_allow_html=True)
        st.info("**3학년 8반** (농구 우승)")
        
    with col3:
        st.markdown("<h3 style='text-align: center; color: #CD7F32;'>🥉 마스터 (3위)</h3>", unsafe_allow_html=True)
        st.warning("**2학년 4반** (계주 1위)")

    st.divider()

    # 5. 참여 유도 이벤트 (인스타그램 태그)
    st.markdown("### 📸 체육대회 인생샷 이벤트")
    st.write("우승/준우승 팀의 멋진 사진이나, 재미있는 응원 사진을 인스타에 올려주세요!")
    st.code("@ganghwa_event_official 태그 필수! #강화고체육대회 #오운완", language="markdown")
    
    # 큼직하고 누르고 싶은 버튼
    if st.button("👉 인스타그램 공식 계정 바로가기", use_container_width=True):
        st.write("*(실제 배포 시 인스타그램 링크로 연결됩니다)*")
