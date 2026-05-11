import streamlit as st
import datetime

def show_page():
    st.markdown("<h1 style='text-align: center; color: #2C3E50;'>📚 제 N회 청람 학술제</h1>", unsafe_allow_html=True)
    
    # 선생님 한마디
    teacher_quote = "비판적 탐구와 깊이 있는 사고가 여러분의 미래를 만듭니다. 화이팅!"
    st.info(f"📢 **응원의 한마디:** {teacher_quote}")

    # --- [핵심] 신청 및 계획서 제출 단계 로직 ---
    st.markdown("### 📝 현재 진행 단계: 계획서 작성 및 제출")
    
    deadline = datetime.date(2026, 5, 12)
    today = datetime.date.today()
    days_left = (deadline - today).days

    if days_left > 0:
        st.warning(f"⏰ **계획서 제출 마감까지 {days_left}일 남았습니다!** (마감일: 5월 12일)")
    elif days_left == 0:
        st.error("🔥 **오늘은 계획서 제출 마감일입니다!** 서둘러 제출해 주세요.")
    else:
        st.success("✅ 계획서 제출이 마감되었습니다. 다음 단계를 기다려 주세요.")

    st.divider()

    # 우진이네 사이트 연동 (보고서 첨삭 서비스)
    st.markdown("### 🤖 AI 보고서 첨삭 서비스")
    st.write("고급 프롬프트로 무장한 AI가 여러분의 학술제 보고서를 더 완벽하게 만들어 드립니다.")
    st.link_button("✨ AI 첨삭 받으러 가기 (우진이네 사이트)", "https://your-friend-woojin-site.com") 
    
    st.divider()

    # 학술제 세션 정보 (어디서 무엇을 들을 수 있나)
    st.markdown("### 🎤 강연 및 발표 세션 안내")
    with st.expander("📍 세션별 장소 및 주제 확인하기"):
        st.write("🏛️ **제1컨퍼런스룸:** AI와 미래 사회 (IT 동아리)")
        st.write("🧪 **과학실1:** 바이오 테크놀로지의 진화 (생명과학 동아리)")
        st.write("⚖️ **사회과학실:** 현대 철학의 쟁점 토론 (인문학 동아리)")

    # 듣고 싶은 세션 신청 폼
    st.markdown("### 🙋‍♂️ 강연 참여 신청")
    with st.form("academic_signup"):
        st.text_input("학번과 이름을 입력하세요 (예: 30508 김지성)")
        st.multiselect("참여하고 싶은 세션을 선택하세요 (최대 2개)", 
                       ["AI와 미래 사회", "바이오 테크놀로지", "현대 철학 쟁점"])
        if st.form_submit_button("신청하기"):
            st.balloons()
            st.success("세션 참여 신청이 완료되었습니다!")

    st.divider()

    # 학술제 의의 및 주의사항
    with st.expander("ℹ️ 학술제 주의사항 및 행사 의의"):
        st.write("**[행사 의의]**")
        st.write("청람 학술제는 학생 스스로 탐구 주제를 설정하고 연구하여 학문적 역량을 기르는 강화고의 전통 깊은 행사입니다.")
        st.write("**[주의사항]**")
        st.write("1. 모든 보고서는 표절 검사 시스템을 거칩니다.")
        st.write("2. 발표 세션 중에는 정숙을 유지하며 적극적으로 질문해 주세요.")
