import streamlit as st
import datetime
import pandas as pd

def initialize_data():
    if 'matches' not in st.session_state:
        st.session_state.matches = [
            {"id": 1, "time": "09:00", "grade": 1, "event": "축구 결승", "team_a": "1반", "team_b": "2반", "winner": None, "points": 100},
            {"id": 2, "time": "09:00", "grade": 2, "event": "농구 결승", "team_a": "3반", "team_b": "4반", "winner": None, "points": 100},
            {"id": 3, "time": "09:50", "grade": 2, "event": "축구 결승", "team_a": "1반", "team_b": "5반", "winner": None, "points": 100},
            {"id": 4, "time": "09:50", "grade": 3, "event": "농구 결승", "team_a": "2반", "team_b": "8반", "winner": None, "points": 100},
            {"id": 5, "time": "11:20", "grade": 3, "event": "축구 결승", "team_a": "5반", "team_b": "8반", "winner": None, "points": 100},
            {"id": 6, "time": "11:20", "grade": 1, "event": "농구 결승", "team_a": "3반", "team_b": "6반", "winner": None, "points": 100},
            {"id": 7, "time": "14:10", "grade": 3, "event": "줄다리기 결승", "team_a": "3반", "team_b": "7반", "winner": None, "points": 50},
        ]

def get_match_status(match_time_str, winner):
    now = datetime.datetime.now().strftime("%H:%M")
    
    if winner:
        return f"✅ 종료 ({winner} 승리)"
    elif now >= match_time_str:
        return "🔥 진행 중"
    else:
        return "⏳ 예정"

def calculate_rankings(grade):
    scores = {}
    for m in st.session_state.matches:
        if m["grade"] == grade and m["winner"]:
            scores[m["winner"]] = scores.get(m["winner"], 0) + m["points"]
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)

def show_page():
    initialize_data()
    
    kiosk_mode = st.toggle("🖥️ 전광판 모드 (전체화면)", value=False)
    
    if kiosk_mode:
        # ==========================================
        # 🖥️ 전광판(Kiosk) 모드
        # ==========================================
        st.markdown("""
            <style>
                [data-testid="stSidebar"] {display: none;}
                .block-container {padding-top: 1rem; padding-bottom: 0rem; max-width: 100%;}
                header {visibility: hidden;}
            </style>
        """, unsafe_allow_html=True)

        st.markdown("<h1 style='text-align: center; font-size: 3rem; color: #1E90FF;'>⚡ 2026 강화고 체육대회 LIVE ⚡</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; margin-top: 30px;'>🎯 경기 실시간 상황</h2>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        cols = [col1, col2, col3]
        
        for i, m in enumerate(st.session_state.matches):
            status = get_match_status(m["time"], m["winner"])
            with cols[i % 3]:
                if "진행 중" in status:
                    st.error(f"[{m['time']}] {m['grade']}학년 {m['event']}\n\n**{m['team_a']} vs {m['team_b']}**\n\n{status}")
                elif "종료" in status:
                    st.success(f"[{m['time']}] {m['grade']}학년 {m['event']}\n\n**{status}**")
                else:
                    st.info(f"[{m['time']}] {m['grade']}학년 {m['event']}\n\n{m['team_a']} vs {m['team_b']}\n\n{status}")
        
    else:
        # ==========================================
        # 📱 일반(모바일) 모드
        # ==========================================
        st.markdown("<h1 style='text-align: center; color: #1E90FF;'>🏆 2026 강화고 체육대회 🏆</h1>", unsafe_allow_html=True)
        
        tab_all, tab_1, tab_2, tab_3 = st.tabs(["🌐 전체 일정", "🐣 1학년", "🐥 2학년", "🦅 3학년"])

        with tab_all:
            st.markdown("### 📅 체육대회 전체 일정표 (공식)")
            
            # [수정됨] 사진의 일정표와 100% 일치하도록 업데이트된 데이터
            schedule_data = {
                "시간": [
                    "08:40 ~ 09:00", "09:00 ~ 09:50", "09:50 ~ 10:40", "10:40 ~ 11:20",
                    "11:20 ~ 12:10", "12:10 ~ 13:00", "13:00 ~ 13:20", "13:20 ~ 13:50",
                    "13:50 ~ 14:10", "14:10 ~ 14:40", "14:40 ~ 15:00", "15:00 ~ 15:30",
                    "15:30 ~ 15:50", "15:50 ~", "16:00 ~"
                ],
                "종목": [
                    "개회식 및 생활안전교육, 준비운동",
                    "1학년 축구 결승 / 2학년 농구 결승",
                    "2학년 축구 결승 / 3학년 농구 결승",
                    "줄다리기 예선",
                    "3학년 축구 결승 / 1학년 농구 결승",
                    "점심시간 🍱",
                    "이벤트 경기 - 장애물 달리기, 줄다리기",
                    "8자 줄넘기, 2단 뛰기(쌩쌩이)",
                    "이벤트 경기 - 학부모 교직원 줄다리기",
                    "줄다리기 결승",
                    "사제 간 경기 (축구)",
                    "계주 예선, 결승",
                    "성적발표, 시상식 및 폐회식",
                    "정리 및 대청소",
                    "2026학년도 읽걷쓰AI 선언식"
                ],
                "참가대상": [
                    "전교생", "1, 2학년", "2, 3학년", "1, 2, 3학년", "1, 3학년",
                    "1, 2, 3학년", "교직원", "1, 2, 3학년", "학부모, 교직원",
                    "1, 2, 3학년", "교직원 vs 학생회", "1, 2, 3학년",
                    "전교생", "전교생", "희망자"
                ]
            }
            # 인덱스를 숨기고 너비를 화면에 맞춤
            st.dataframe(pd.DataFrame(schedule_data), hide_index=True, use_container_width=True)

        for g_idx, tab in enumerate([tab_1, tab_2, tab_3], start=1):
            with tab:
                st.markdown(f"### 🔥 {g_idx}학년 실시간 경기 현황")
                for m in st.session_state.matches:
                    if m["grade"] == g_idx:
                        status = get_match_status(m["time"], m["winner"])
                        st.write(f"**{m['time']} | {m['event']}** ({m['team_a']} vs {m['team_b']}) ➔ {status}")
                
                st.divider()
                st.markdown(f"#### 👑 {g_idx}학년 종합 순위 (우승 유력)")
                rankings = calculate_rankings(g_idx)
                if rankings:
                    for i, (team, score) in enumerate(rankings):
                        medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉"
                        st.write(f"{medal} **{team}**: {score}점")
                else:
                    st.write("아직 점수를 획득한 반이 없습니다.")

        st.divider()
        # ==========================================
        # 🔐 운영진 전용 (관리자 로그인 시스템)
        # ==========================================
        if 'admin_logged_in' not in st.session_state:
            st.session_state.admin_logged_in = False

        with st.expander("🔐 운영진 전용 (Staff Only)"):
            if not st.session_state.admin_logged_in:
                admin_pw = st.text_input("관리자 암호를 입력하세요", type="password")
                if st.button("접속"):
                    if admin_pw == "0409": 
                        st.session_state.admin_logged_in = True
                        st.rerun() 
                    else:
                        st.error("암호가 틀렸습니다. 접근 권한이 없습니다.")
            
            else:
                col1, col2 = st.columns([0.8, 0.2])
                with col1:
                    st.success("✅ 운영진 모드 활성화됨")
                with col2:
                    if st.button("로그아웃"):
                        st.session_state.admin_logged_in = False
                        st.rerun()

                st.warning("이곳에서 승리 팀을 선택하면 전광판과 일반 모드의 점수가 즉시 변동됩니다.")
                
                for i, m in enumerate(st.session_state.matches):
                    winner_choice = st.radio(
                        f"{m['grade']}학년 {m['event']} ({m['time']})",
                        options=["선택 안함", m['team_a'], m['team_b']],
                        index=0 if m['winner'] is None else (1 if m['winner'] == m['team_a'] else 2),
                        key=f"match_{i}"
                    )
                    
                    new_winner = None if winner_choice == "선택 안함" else winner_choice
                    if st.session_state.matches[i]["winner"] != new_winner:
                        st.session_state.matches[i]["winner"] = new_winner
                        st.rerun()
