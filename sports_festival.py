import streamlit as st
import datetime
import pandas as pd

def show_page():
    # [핵심] 모드 전환 토글 (가장 위에 배치)
    kiosk_mode = st.toggle("🖥️ 전광판 모드 (전체화면)", value=False)
    
    # ==========================================
    # 🖥️ 전광판(Kiosk) 모드: CSS로 화면 꽉 차게 만들기
    # ==========================================
    if kiosk_mode:
        # 1. CSS 주입: 사이드바 숨기기, 상단 여백 없애기, 스트림릿 기본 헤더 숨기기
        st.markdown("""
            <style>
                [data-testid="stSidebar"] {display: none;}
                .block-container {padding-top: 1rem; padding-bottom: 0rem; max-width: 100%;}
                header {visibility: hidden;}
                /* 탭 글씨 크기 키우기 */
                .stTabs [data-baseweb='tab-list'] button {font-size: 1.5rem; font-weight: bold;}
            </style>
        """, unsafe_allow_html=True)

        k_tab_all, k_tab_1, k_tab_2, k_tab_3 = st.tabs(["🌐 종합 순위", "🐣 1학년", "🐥 2학년", "🦅 3학년"])
        
        with k_tab_1:
            st.markdown("<h1 style='text-align: center; font-size: 4rem; color: #FFD700; margin-top: 50px;'>🐣 1학년 경기 현황</h1>", unsafe_allow_html=True)
            st.markdown("<h2 style='text-align: center; font-size: 3rem;'>🔥 피구/발야구 예선 진행 중!</h2>", unsafe_allow_html=True)

        with k_tab_2:
            st.markdown("<h1 style='text-align: center; font-size: 4rem; color: #32CD32; margin-top: 20px;'>🐥 2학년 경기 현황</h1>", unsafe_allow_html=True)
            st.markdown("<h2 style='text-align: center; font-size: 3rem; color: #e74c3c;'>🏀 다음 결승: 2-1 vs 2-4 (15:30)</h2>", unsafe_allow_html=True)
            st.markdown("""
            <div style="display: flex; justify-content: center; gap: 30px; margin-top: 40px;">
                <div style="font-size: 3.5rem; background: white; padding: 30px; border-radius: 20px; border: 5px solid #FFD700;">🥇 2-4 (210점)</div>
                <div style="font-size: 3.5rem; background: white; padding: 30px; border-radius: 20px; border: 5px solid #C0C0C0;">🥈 2-1 (180점)</div>
            </div>
            """, unsafe_allow_html=True)

        with k_tab_3:
            st.markdown("<h1 style='text-align: center; font-size: 4rem; color: #FF4500; margin-top: 20px;'>🦅 3학년 경기 현황</h1>", unsafe_allow_html=True)
            st.markdown("<h2 style='text-align: center; font-size: 3rem; color: #3498db;'>⚽ 현재 진행 중: 3-5 vs 3-8 축구 결승</h2>", unsafe_allow_html=True)
            st.markdown("""
            <div style="display: flex; justify-content: center; gap: 30px; margin-top: 40px;">
                <div style="font-size: 3.5rem; background: white; padding: 30px; border-radius: 20px; border: 5px solid #FFD700;">🥇 3-5 (350점)</div>
                <div style="font-size: 3.5rem; background: white; padding: 30px; border-radius: 20px; border: 5px solid #C0C0C0;">🥈 3-8 (280점)</div>
            </div>
            """, unsafe_allow_html=True)

    # ==========================================
    # 📱 일반(모바일) 모드
    # ==========================================
    else:
        st.markdown("<h1 style='text-align: center; color: #1E90FF;'>🏆 2026 강화고 체육대회 🏆</h1>", unsafe_allow_html=True)
        st.info("📢 **기선쌤의 한마디:** 다치지 말고 체육대회 모두 파이팅~ 👊")
        st.divider()

        tab_all, tab_1, tab_2, tab_3 = st.tabs(["🌐 전체 보기", "🐣 1학년", "🐥 2학년", "🦅 3학년"])

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

        with tab_1:
            st.markdown("### 🐣 1학년 경기 현황")
            st.error("오전 예선 진행 중입니다. 결승 매치업이 확정되면 업데이트됩니다.")

        with tab_2:
            st.markdown("### 🐥 2학년 결승 매치업")
            st.warning("🏀 **농구 결승:** 2-1 vs 2-4 (15:30 @실내체육관)")
            st.warning("🏃 **계주 결승:** 2학년 대표 선발 완료 (16:30 @대운동장)")
            st.divider()
            st.markdown("#### 👑 2학년 명예의 전당")
            col1, col2 = st.columns(2)
            col1.metric("🥇 1위", "2학년 4반", "농구 결승 진출")
            col2.metric("🥈 2위", "2학년 1반", "계주 점수 합산 대기")

        with tab_3:
            st.markdown("### 🦅 3학년 결승 매치업")
            st.success("⚽ **축구 결승:** 3-5 vs 3-8 (14:00 @대운동장)")
            st.divider()
            st.markdown("#### 👑 3학년 명예의 전당")
            col1, col2 = st.columns(2)
            col1.metric("🥇 1위", "3학년 5반", "축구 우승 유력")
            col2.metric("🥈 2위", "3학년 8반", "축구 준우승")
