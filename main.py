import streamlit as st

def show_page():
    # 1. 알록달록한 타이틀과 인사말
    st.title("🎪 마리마당 축제에 오신걸 환영해요! 🎈")
    st.markdown("### ✨ 반짝반짝 신나는 하루를 만들어봐요! ✨")
    
    st.divider() # 귀여운 구분선

    # 2. 스케치하신 4개의 메인 메뉴 (컬러풀한 박스 활용)
    st.markdown("#### 🎡 무엇을 알아볼까요?")
    col1, col2 = st.columns(2)

    with col1:
        # success = 초록색 박스
        st.success("🗓️ **축제 일정 전체보기**\n\n오늘의 주요 행사 및 공연 시간 확인")
        # info = 파란색 박스
        st.info("🎤 **장기자랑 무대 신청**\n\n신청 기간 및 방법, 참가 자격 확인")

    with col2:
        # warning = 노란색 박스
        st.warning("🍔 **인기 부스 & 푸드트럭**\n\n전체 부스 위치 및 운영 시간 확인")
        # error = 빨간색 박스
        st.error("📢 **공지사항 및 안내**\n\n건의 사항 수집 및 비상 연락망")

    st.divider()

    # 3. 장기자랑 신청 폼 (UI 껍데기 - 나중에 DB랑 연결할 부분)
    st.markdown("### 🌟 나도 무대 주인공! 장기자랑 신청하기 🌟")
    
    with st.form("talent_show_form"):
        st.text_input("학번과 이름을 적어주세요! (예: 30508 김지성) 🎒")
        st.selectbox("어떤 장기를 보여줄 건가요? 🎤", ["춤 💃", "노래 🎵", "랩 🎤", "악기 연주 🎸", "기타 🤹‍♂️"])
        st.text_area("공연할 곡 제목이나 간단한 설명을 적어주세요! 📝")
        
        # 알록달록한 제출 버튼
        submitted = st.form_submit_button("✨ 신청서 날리기! 🚀")
        
        if submitted:
            # 제출 버튼을 누르면 화면에 진짜 풍선이 날아갑니다! (초딩 감성 핵심)
            st.balloons() 
            st.success("우와! 신청이 완료되었어요! 🎉 (※ 지금은 UI 테스트 중입니다)")
