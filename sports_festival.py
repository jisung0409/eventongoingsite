import streamlit as st
import datetime
import pandas as pd

def show_page():
    # 1. 상단 토글 스위치 (전광판 모드 vs 일반 모드)
    st.markdown("<br>", unsafe_allow_html=True)
    kiosk_mode = st.toggle("🖥️ 스탠드/본부석 전광판 모드 켜기", value=False)
    st.divider()

    # ==========================================
    # 🖥️ 전광판(Kiosk) 모드 (본부석 노트북 거치용)
    # ==========================================
    if kiosk_mode:
        # 글씨를 큼직하게 키우고 불필요한 설명은 다 뺌
        st.markdown("<h1 style='text-align: center; font-size: 3rem; color: #1E90FF;'>⚡ LIVE: 체육대회 현황 ⚡</h1>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 👉 지금 진행 중인 경기")
            st.error("⚽ **축구 결승**\n\n 3-5 vs 3-8 (대운동장)")
        with col2:
            st.markdown("### 👉 다음 경기 (15:30)")
            st.warning("🏀 **농구 결승**\n\n 2-1 vs 2-4 (체육관)")
            
        st.divider()
        st.markdown("<h2 style='text-align: center;'>👑 실시간 종합 순위</h2>", unsafe_allow_html=True)
        
        # st.metric을 사용해 숫자(점수)를 강조하는 대시보드 형태
        score1, score2, score3 = st.columns(3)
        score1.metric(label="🥇 1위 (3학년 5반)", value="350점", delta="축구 우승 (+100)")
        score2.metric(label="🥈 2위 (3학년 8반)", value="280점", delta="농구 우승 (+80)")
        score3.metric(label="🥉 3위 (2학년 4반)", value="210점", delta="계주 1위 (+50)")

    # ==========================================
    # 📱 일반(모바일) 모드 (체육대회 전/후 접속용)
    # ==========================================
    else:
        st.markdown("<h1 style='text-align: center; color: #1E90FF;'>🏆 2026 강화고 체육대회 🏆</h1>", unsafe_allow_html=True)
        st.info("📢 **기선쌤의 한마디:** 다치지 말고 체육대회 모두 파이팅~ 👊")
        
        # [신규 추가] 사전 트래픽 유도용: 우승팀 예측 투표
        st.markdown("### 🔥 [사전 이벤트] 종목별 우승팀을 맞춰라!")
        with st.form("prediction_form"):
            st.write("가장 치열할 것 같은 경기의 승자를 예측해 보세요! (적중 시 추첨을 통해 매점 쿠폰 증정)")
            pred_soccer = st.selectbox("⚽ 축구 결승 승리팀 예측", ["3학년 5반", "3학년 8반", "모르겠음(기권)"])
            pred_basketball = st.selectbox("🏀 농구 결승 승리팀 예측", ["2학년 1반", "2학년 4반", "모르겠음(기권)"])
            
            student_id = st.text_input("경품 수령용 학번 (예: 30508)")
            
            if st.form_submit_button("예측 투표 날리기 🚀"):
                if student_id:
                    st.balloons()
                    st.success("투표가 완료되었습니다! 체육대회 당일 결과를 확인하세요.")
                else:
                    st.error("경품을 받으려면 학번을 꼭 적어주세요!")

        st.divider()

        # 기존 시간표 및 정보 (아코디언으로 숨겨서 스크롤 최소화)
        with st.expander("📅 체육대회 전체 시간표 보기"):
            schedule_data = {
                "시간": ["09:00", "10:00", "12:00", "13:00", "15:00", "16:30"],
                "운동장": ["개회식", "축구 예선", "점심시간", "축구 결승", "전학년 계주", "폐회식"],
                "체육관": ["-", "배드민턴", "점심시간", "농구 결승", "축하공연", "-"]
            }
            st.table(pd.DataFrame(schedule_data))
        
        with st.expander("📸 체육대회 인생샷 이벤트 안내"):
            st.write("우승/준우승 팀의 멋진 사진이나, 재미있는 응원 사진을 인스타에 올려주세요!")
            st.code("@ganghwa_event_official 태그 필수!", language="markdown")
            
