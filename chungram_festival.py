import streamlit as st
import datetime
import pandas as pd

def show_page():
    # ==========================================
    # 🎨 학술활동지원시스템(외부 사이트) 감성 맞춤 CSS
    # ==========================================
    st.markdown("""
        <style>
            /* 부드러운 모서리의 흰색 카드 UI */
            .cr-card {
                background-color: #ffffff;
                border-radius: 16px;
                padding: 24px;
                box-shadow: 0 4px 14px rgba(0,0,0,0.03);
                border: 1px solid #f3f4f6;
                margin-bottom: 20px;
            }
            .cr-title {
                color: #1f2937;
                font-size: 1.25rem;
                font-weight: 700;
                margin-bottom: 12px;
                border-bottom: 2px solid #f3f4f6;
                padding-bottom: 8px;
            }
            .cr-text {
                color: #4b5563;
                font-size: 0.95rem;
                line-height: 1.6;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center; color: #111827; margin-top: -20px; font-weight: 800;'>🌐 제1회 청람학술제</h1>", unsafe_allow_html=True)
    st.write("---")
    
    # ==========================================
    # 📖 1. 청람학술제 역사와 의의 (소개글)
    # ==========================================
    st.markdown("""
        <div class="cr-card">
            <div class="cr-title">📚 청람학술제란? (역사와 의의)</div>
            <div class="cr-text">
                <b>'청출어람(靑出於藍)'</b>의 정신을 잇는 강화고등학교 청람학술제는 학생들의 자기주도적 탐구 역량과 
                비판적 사고력을 기르기 위해 마련된 지식의 장입니다.<br><br>
                단순히 교과 지식을 암기하는 것을 넘어, 학생들이 직접 실생활의 문제를 발굴하고 창의적인 해결책을 
                모색하는 과정을 통해 <b>미래 사회를 이끌어갈 융합형 인재</b>로 성장하는 것을 목표로 합니다. 
                선후배와 동기간의 학술적 교류를 통해 지식의 폭을 넓히고, 협업의 가치를 배우는 강화고 최고의 학술 축제에 여러분을 초대합니다.
            </div>
        </div>
    """, unsafe_allow_html=True)

    # ==========================================
    # 🔗 2. 학술활동지원시스템 외부 링크 (친구분 사이트)
    # ==========================================
    st.markdown("### 💻 조별 활동 및 보고서 작성")
    st.info("💡 팀원들과의 원활한 소통, 계획서 제출, 그리고 보고서 첨삭은 **학술활동지원시스템**에서 진행됩니다.")
    
    # 외부 사이트로 이동하는 버튼 (새 탭에서 열림)
    st.link_button(
        "📝 청람학술제 학술활동지원시스템으로 이동하기 ➔", 
        "https://cheongram-git-dev-cheongram.vercel.app", 
        use_container_width=True,
        type="primary"
    )
    
    st.write("---")

    # ==========================================
    # 📌 3. 현재 진행 단계 및 서류 제출 현황
    # ==========================================
    col_info, col_dead = st.columns(2)
    
    with col_info:
        st.markdown("""
            <div class="cr-card" style="height: 100%;">
                <div class="cr-title">📢 진행 단계 안내</div>
                <div class="cr-text">
                    현재 청람학술제는 <b>[강연 및 발표 세션 안내 / 가신청 단계]</b>입니다. 하단의 주제 목록을 읽고 본인이 들을 세션을 골라주세요.
                </div>
            </div>
        """, unsafe_allow_html=True)
        
    with col_dead:
        st.markdown("""
            <div class="cr-card" style="height: 100%; border-left: 4px solid #ef4444;">
                <div class="cr-title" style="color: #ef4444;">📄 서류 제출 마감</div>
                <div class="cr-text">
                    <b>⏳ 계획서 및 연구 보고서 제출 기한이 만료되었습니다.</b><br><br>
                    시스템을 통한 추가 제출 및 수정은 불가능합니다. (관련 문의는 학술제 운영진에게 연락 바랍니다)
                </div>
            </div>
        """, unsafe_allow_html=True)
        
    st.write("---")
    
    # ==========================================
    # 🎤 4. 강연 및 발표 세션 안내
    # ==========================================
    st.markdown("### 🎤 강연 및 발표 세션 안내")
    st.markdown("<span style='color:#6b7280;'>올해 청람학술제에서 진행되는 다채로운 강연 주제입니다. **각 주제를 클릭**하시면 간단한 세션 설명을 보실 수 있습니다.</span>", unsafe_allow_html=True)
    
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
    
    st.write("")
    for topic in lecture_topics:
        with st.expander(topic["title"]):
            st.markdown(f"<div style='line-height:1.6; color:#4b5563; padding: 5px;'>{topic['desc']}</div>", unsafe_allow_html=True)
            st.markdown("<span style='color:#f59e0b; font-size:0.85rem;'>* 본 강연은 선착순으로 좌석이 조기 마감될 수 있습니다.</span>", unsafe_allow_html=True)
            
    st.write("---")
    
    # ==========================================
    # ✍️ 5. 발표 세션 신청창 레이아웃 (학번/이름 분리)
    # ==========================================
    st.markdown("### ✍️ 발표 세션 가신청하기")
    st.caption("※ 인당 최대 이수 가능 세션 수가 확정되지 않아, 현재는 희망 종목 복수 선택(가신청)이 가능하도록 열려 있습니다.")
    
    with st.form("chungram_application_form"):
        c_id, c_name = st.columns(2)
        with c_id:
            student_id = st.text_input("학번 입력 (5자리)", placeholder="예: 30508", max_chars=5)
        with c_name:
            student_name = st.text_input("이름 입력", placeholder="예: 홍길동")
            
        st.write("")
        st.markdown("#### 📚 수강 희망 세션 선택 (중복 가능)")
        
        options_list = [l["title"] for l in lecture_topics]
        selected_lectures = st.multiselect(
            "안내 탭에서 확인한 희망 강연을 모두 체크해 주세요.",
            options=options_list,
            placeholder="여기를 클릭하여 강연 주제를 선택하세요"
        )
        
        st.write("")
        submit_button = st.form_submit_button("🚀 학술제 가신청서 임시 제출", use_container_width=True)
        
        if submit_button:
            if not student_id.strip() or not student_name.strip():
                st.error("❌ 신청 실패: 학번과 이름을 빠짐없이 입력해 주세요.")
            elif not selected_lectures:
                st.warning("⚠️ 신청 불가: 수강할 강연 세션을 최소 1개 이상 선택해 주세요.")
            else:
                st.success(f"🎉 가신청 완료: **{student_name} ({student_id})** 학생의 가신청서가 임시 접수되었습니다.")
                st.markdown(f"**선택한 강연 ({len(selected_lectures)}건):**")
                for sel in selected_lectures:
                    st.write(f"- {sel}")
