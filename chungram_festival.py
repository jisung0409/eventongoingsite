import streamlit as st
import datetime
import pandas as pd

def show_page():
    st.markdown("<h1 style='text-align: center; color: #4A90E2; margin-top: -20px;'>🌐 제1회 청람학술제</h1>", unsafe_allow_html=True)
    st.write("---")
    
    # ==========================================
    # 📌 1. 현재 진행 단계 및 서류 제출 현황
    # ==========================================
    col_info, col_dead = st.columns(2)
    
    with col_info:
        st.markdown("### 📢 진행 단계 안내")
        st.info("현재 청람학술제는 **[강연 및 발표 세션 안내 / 가신청 단계]**입니다. 하단의 주제 목록을 읽고 본인이 들을 세션을 골라주세요.")
        
    with col_dead:
        st.markdown("### 📄 학술제 서류 제출")
        # 계획서 및 보고서 제출 기한 마감 상태 고정
        st.error("⏳ **계획서 및 연구 보고서 제출 기한이 만료되었습니다.**\n\n시스템을 통한 추가 제출 및 수정은 불가능합니다. (운영진 문의)")
        
    st.write("---")
    
    # ==========================================
    # 🎤 2. 강연 및 발표 세션 안내 (주제별 설명 추가)
    # ==========================================
    st.markdown("### 🎤 강연 및 발표 세션 안내")
    st.markdown("올해 청람학술제에서 진행되는 다채로운 강연 주제입니다. **각 주제를 클릭**하시면 간단한 세션 설명을 보실 수 있습니다.")
    
    # 학술제 강연 주제 및 간단한 요약 데이터셋
    # (추후 구글 시트 양식에 맞춰 불러오거나 직접 텍스트를 수정할 수 있습니다!)
    lecture_topics = [
        {
            "title": "🤖 인공지능 프롬프트 엔지니어링과 미래 보안 기술",
            "desc": "딥페이크 식별을 위한 SynthID 기술 및 인공지능 오남용 방지를 위한 최신 하드웨어 암호화 및 아키텍처 보안 전략을 알아봅니다."
        },
        {
            "title": "💻 오픈소스 파이썬 라이브러리를 활용한 데이터 자동화 개발",
            "desc": "Pandas와 Streamlit을 활용하여 학교 생활이나 동아리 활동에 직접 써먹을 수 있는 유용한 웹 애플리케이션 프레임워크 설계 기법을 배웁니다."
        },
        {
            "title": "🔐 블록체인과 현대 암호학: 분산원장의 인증 메커니즘",
            "desc": "중앙 서버 없는 분산형 데이터 네트워크의 무결성 검증 원리를 파악하고, 차세대 인증 프레임워크의 취약점을 분석합니다."
        },
        {
            "title": "🌍 공간 빅데이터로 풀어내는 우리 지역 사회의 당면 과제",
            "desc": "지리 정보 시스템(GIS) 데이터와 공공 API를 매핑하여 교내 교통 안전, 지역 상권 상생 등 실질적인 사회 현제를 공학적으로 접근합니다."
        }
    ]
    
    # Expander 컴포넌트를 사용하여 가독성 확보 및 상세 설명 매핑
    for topic in lecture_topics:
        with st.expander(topic["title"]):
            st.markdown(f"<div style='line-height:1.6; color:#333; padding: 5px;'>{topic['desc']}</div>", unsafe_allow_html=True)
            st.markdown("<span style='color:#e28743; font-size:0.85rem;'>* 본 강연은 선착순으로 좌석이 조기 마감될 수 있습니다.</span>", unsafe_allow_html=True)
            
    st.write("---")
    
    # ==========================================
    # ✍️ 3. 발표 세션 신청창 레이아웃 (학번/이름 분리)
    # ==========================================
    st.markdown("### ✍️ 발표 세션 가신청하기")
    st.caption("※ 인당 최대 이수 가능 세션 수가 아직 확정되지 않아, 현재는 희망 종목 복수 선택(가신청)이 가능하도록 열려 있습니다.")
    
    # 가신청 입력을 위한 독립 폼 구성
    with st.form("chungram_application_form"):
        # 학번과 이름을 독립된 칸으로 분리 입력받음
        c_id, c_name = st.columns(2)
        with c_id:
            student_id = st.text_input("학번 입력 (5자리)", placeholder="예: 30508", max_chars=5)
        with c_name:
            student_name = st.text_input("이름 입력", placeholder="예: 김지성")
            
        st.write("")
        st.markdown("#### 📚 수강 희망 세션 선택 (중복 가능)")
        
        # 선택 옵션 리스트 추출
        options_list = [l["title"] for l in lecture_topics]
        selected_lectures = st.multiselect(
            "안내 탭에서 확인한 희망 강연을 모두 체크해 주세요.",
            options=options_list,
            placeholder="여기를 클릭하여 강연 주제를 선택하세요"
        )
        
        st.write("")
        submit_button = st.form_submit_button("🚀 학술제 가신청서 제출하기", use_container_width=True)
        
        if submit_button:
            if not student_id.strip() or not student_name.strip():
                st.error("❌ 신청 실패: 학번과 이름을 빠짐없이 입력해 주세요.")
            elif not selected_lectures:
                st.warning("⚠️ 신청 불가: 수강할 강연 세션을 최소 1개 이상 선택해 주세요.")
            else:
                # 데이터베이스 연동 전 임시 검증 출력 블록
                st.success(f"🎉 가신청 완료: **{student_name} ({student_id})** 학생의 가신청서가 임시 접수되었습니다.")
                st.markdown(f"**선택한 강연 ({len(selected_lectures)}건):**")
                for sel in selected_lectures:
                    st.write(f"- {sel}")
