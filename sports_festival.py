import streamlit as st
import datetime
import pandas as pd

def show_page():
    # 1. 상단 공통 헤더
    st.markdown("<h1 style='text-align: center; color: #1E90FF;'>🏆 2026 강화고 체육대회 🏆</h1>", unsafe_allow_html=True)
    st.info("📢 **기선쌤의 한마디:** 다치지 말고 체육대회 모두 파이팅~ 👊")
    
    kiosk_mode = st.toggle("🖥️ 스탠드/본부석 전광판 모드 켜기", value=False)
    st.divider()

    # ==========================================
    # 🖥️ 전광판(Kiosk) 모드 (본부석 노트북 거치용)
    # ==========================================
    if kiosk_mode:
        st.markdown("<h1 style='text-align: center; font-size: 3rem; color: #1E90FF;'>⚡ LIVE: 종합 스코어보드 ⚡</h1>", unsafe_allow_html=True)
        # 전광판은 전체 학년의 굵직한 점수만 보여줍니다.
        score1, score2, score3 = st.columns(3)
        score1.metric(label="🥇 종합 1위 (3-5)", value="350점", delta="축구 우승 (+100)")
        score2.metric(label="🥈 종합 2위 (3-8)", value="280점", delta="농구 우승 (+80)")
        score3.metric(label="🥉 종합 3위 (2-4)", value="210점", delta="계주 1위 (+50)")

    # ==========================================
    # 📱 일반(모바일) 모드 - 탭(Tabs)을 이용한 학년별 분리
    # ==========================================
    else:
        # [핵심] 4개의 탭 생성
        tab_all, tab_1, tab_2, tab_3 = st.tabs(["🌐 전체 보기", "🐣 1학년", "🐥 2학년", "🦅 3학년"])

        # --- 1. 첫 번째 탭: 전체 종합 정보 ---
        with tab_all:
            st.markdown("### 📅 체육대회 전체 시간표")
            schedule_data = {
                "시간": ["09:00 - 10:00", "10:00 - 12:00", "13:00 - 15:00", "15:00 - 16:30"],
                "운동장": ["개회식", "학년별 예선", "종목별 결승", "전학년 계주"],
                "체육관": ["-", "배드민턴", "농구 결승", "축하공연"]
            }
            st.table(pd.DataFrame(schedule_data))
            
            st.markdown("### 🔥 [이벤트] 종합 우승반 예측 투표")
            with st.form("prediction_form"):
                st.selectbox("올해의 강화고 종합 우승 반은?", ["1학년 전체", "2학년 4반", "3학년 5반", "3학년 8반"])
                st.text_input("학번 (경품 수령용)")
                if st.form_submit_button("투표하기"):
                    st.success("투표 완료!")

        # --- 2. 두 번째 탭: 1학년 전용 ---
        with tab_1:
            st.markdown("### 🐣 1학년 경기 현황")
            st.error("오전 예선 진행 중입니다. 결승 매치업이 확정되면 업데이트됩니다.")

        # --- 3. 세 번째 탭: 2학년 전용 ---
        with tab_2:
            st.markdown("### 🐥 2학년 결승 매치업")
            st.warning("🏀 **농구 결승:** 2-1 vs 2-4 (15:30 @실내체육관)")
            st.warning("🏃 **계주 결승:** 2학년 대표 선발 완료 (16:30 @대운동장)")
            
            st.divider()
            st.markdown("#### 👑 2학년 명예의 전당")
            col1, col2 = st.columns(2)
            col1.metric("🥇 1위", "2학년 4반", "농구 결승 진출")
            col2.metric("🥈 2위", "2학년 1반", "계주 점수 합산 대기")

        # --- 4. 네 번째 탭: 3학년 전용 ---
        with tab_3:
            st.markdown("### 🦅 3학년 결승 매치업")
            st.success("⚽ **축구 결승:** 3-5 vs 3-8 (14:00 @대운동장)")
            
            st.divider()
            st.markdown("#### 👑 3학년 명예의 전당")
            col1, col2 = st.columns(2)
            col1.metric("🥇 1위", "3학년 5반", "축구 우승 유력")
            col2.metric("🥈 2위", "3학년 8반", "축구 준우승")
