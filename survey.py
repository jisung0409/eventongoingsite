import streamlit as st
import datetime

def show_page():
    # 1. 헤더 영역
    st.markdown("<h1 style='text-align: center; color: #FF6B6B;'>📊 강화고 설문조사 & 아이디어함</h1>", unsafe_allow_html=True)
    st.info("📢 **공지:** 설문에 참여하신 분들 중 추첨을 통해 매주 금요일 매점 쿠폰을 드립니다! (협업 부서: 학생 자치부)")
    st.divider()

    # 2. 이번 주의 설문 (생기부 활동용/재미용)
    st.markdown("### 🔥 이번 주의 Hot Topic")
    with st.container():
        st.write("**Q. 우리 학교 매점에 반드시 추가되었으면 하는 메뉴는?**")
        
        # index=0 으로 기본 선택지를 주어 에러 방지
        choice = st.radio(
            "하나만 골라주세요!",
            ["시원한 제로 콜라🥤", "뜨끈한 피자빵🍕", "달콤한 초코 모찌🍡", "든든한 삼각김밥🍙"],
            index=0 
        )
        
        if st.button("투표하기"):
            st.toast(f"'{choice}'에 투표 완료! 브라우저 쿠키에 기록되었습니다. ✅")
            st.balloons()

    st.divider()

    # 3. 생기부 아이디어 제안 (누군가의 활동용)
    st.markdown("### 💡 우리 학교 행사 아이디어함")
    st.caption("여러분의 반짝이는 아이디어가 실제 행사가 될 수 있습니다!")
    
    with st.form("idea_form"):
        st.write("새로운 행사나 프로그램 아이디어를 들려주세요.")
        idea_title = st.text_input("아이디어 한 줄 제목")
        idea_detail = st.text_area("구체적인 설명 (왜 필요한지, 어떤 활동을 하는지)")
        
        student_id = st.text_input("경품 추첨용 학번 (예: 30508)")
        
        submitted = st.form_submit_button("아이디어 제출 및 경품 응모 🚀")
        
        if submitted:
            if idea_title and student_id:
                st.success(f"제출 완료! {student_id}님, 행운을 빌어요! ✨")
            else:
                st.error("학번과 제목은 꼭 입력해 주세요!")

    st.divider()

    # 4. 명예의 전당 / 지난 설문 결과 (시각화)
    st.markdown("### 📈 지난 설문 결과 보기")
    with st.expander("지난주: '강화고 최고의 점심 메뉴는?' 결과 확인"):
        st.write("1위: 돈까스 (45%)")
        st.progress(0.45)
        st.write("2위: 제육볶음 (30%)")
        st.progress(0.30)
        st.write("3위: 마라탕 (25%)")
        st.progress(0.25)

    st.caption("본 설문 시스템은 '헬로월드' 동아리에서 운영하며, 데이터는 학생 자치 활동 증빙 자료로 활용될 수 있습니다.")
