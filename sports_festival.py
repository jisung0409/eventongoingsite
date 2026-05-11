import streamlit as st
import datetime
import pandas as pd

def show_page():
    # 1. 밝고 에너지 넘치는 헤더 (선명한 파란색 포인트)
    st.markdown("<h1 style='text-align: center; color: #1E90FF;'>🏆 2026 강화고 체육대회 🏆</h1>", unsafe_allow_html=True)
    
    teacher_quote = "다치지 말고 체육대회 모두 파이팅~ 👊"
    st.info(f"📢 **기선쌤의 한마디:** {teacher_quote}")
    st.divider()

    # 2. 행사 진행 상태 체크 로직
    today = datetime.date.today()
    event_end_date = datetime.date(2026, 5, 20)
    
    if today > event_end_date:
        st.error("🏁 올해 체육대회가 모두 종료되었습니다. 내년을 기약해 주세요! ㅠㅠ")
    else:
        st.success("🔥 현재 체육대회가 뜨겁게 진행 중입니다! 🔥")
    
    # 3. 전체 시간표 (표 형식으로 깔끔하게 표시)
    st.markdown("### 📅 체육대회 전체 시간표 (임시)")
    schedule_data = {
        "시간": ["09:00 - 10:00", "10:00 - 12:00", "12:00 - 13:00", "13:00 - 15:00", "15:00 - 16:30", "16:30 - 17:00"],
        "대운동장": ["개회식 및 준비운동", "축구/피구 예선", "점심시간 🍱", "축구 결승전", "전학년 계주", "폐회식 및 시상"],
        "체육관": ["-", "배드민턴 예선", "점심시간 🍱", "농구 결승전", "동아리 축하공연", "-"]
    }
    df_schedule = pd.DataFrame(schedule_data)
    st.table(df_schedule)
    
    st.divider()

    # 4. 결승전 매치업 안내 (아코디언 메뉴)
    st.markdown("### 🗓️ 오늘의 결승전 매치업")
    with st.expander("👉 상세 경기 대진표 보기", expanded=True):
        st.write("⚽ **축구 결승:** 3학년 5반 vs 3학년 8반 (14:00 @대운동장)")
        st.write("🏀 **농구 결승:** 2학년 1반 vs 2학년 4반 (15:30 @실내체육관)")
        st.write("🏃 **계주 결승:** 전 학년 통합 (16:30 @대운동장 트랙)")

    st.divider()

    # 5. 명예의 전당 (밝은 배경에 잘 보이는 색상으로 변경된 게임 티어 시스템)
    st.markdown("### 👑 명예의 전당 (Hall of Fame)")
    st.caption("실시간 종목별 종합 우승 현황입니다.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<h3 style='text-align: center; color: #FF8C00;'>🥇 챌린저 (1위)</h3>", unsafe_allow_html=True)
        st.success("**3학년 5반**\n\n(축구 우승, 계주 2위)")
        
    with col2:
        st.markdown("<h3 style='text-align: center; color: #708090;'>🥈 그랜드마스터 (2위)</h3>", unsafe_allow_html=True)
        st.info("**3학년 8반**\n\n(농구 우승)")
        
    with col3:
        st.markdown("<h3 style='text-align: center; color: #8B4513;'>🥉 마스터 (3위)</h3>", unsafe_allow_html=True)
        st.warning("**2학년 4반**\n\n(계주 1위)")

    st.divider()

    # 6. 인스타그램 참여 유도 이벤트 영역
    st.markdown("### 📸 체육대회 인생샷 이벤트")
    st.write("우승/준우승 팀의 멋진 사진이나, 재미있는 응원 사진을 인스타에 올려주세요!")
    st.code("@ganghwa_event_official 태그 필수! #강화고체육대회", language="markdown")
    
    st.button("👉 인스타그램 공식 계정 바로가기", use_container_width=True)
