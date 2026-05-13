import streamlit as st
import datetime
import pandas as pd

def initialize_data():
    # 데이터베이스 역할을 하는 세션 상태 초기화 (대회 전날 대진표 확정 시 여기에 팀 입력)
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
    # 현재 시간과 경기 시간을 비교하여 상태 반환 (테스트를 위해 현재 시간을 임의로 고정할 수도 있음)
    now = datetime.datetime.now().strftime("%H:%M")
    
    if winner:
        return f"✅ 종료 ({winner} 승리)"
    elif now >= match_time_str:
        return "🔥 진행 중"
    else:
        return "⏳ 예정"

def calculate_rankings(grade):
    # DB(세션)를 순회하며 해당 학년의 점수를 실시간으로 계산
    scores = {}
    for m in st.session_state.matches:
        if m["grade"] == grade and m["winner"]:
            scores[m["winner"]] = scores.get(m["winner"], 0) + m["points"]
    # 점수 높은 순으로 정렬
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)

def show_page():
    initialize_data()
    
    # 상단 토글 스위치
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
        
        # 현재 진행 상황 (가장 직관적으로 표시)
        st.markdown("<h2 style='text-align: center; margin-top: 30px;'>🎯 경기 실시간 상황</h2>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        cols = [col1, col2, col3]
        
        # 전체 경기 중 상태를 띄워줌
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
            st.markdown("### 📅 체육대회 전체 시간표 (공식)")
            # 사진의 시간표를 바탕으로 데이터프레임 구성
            schedule_data = {
                "시간": ["08:40~09:00", "09:00~09:50", "09:50~10:40", "10:40~11:20", "11:20~12:10", "13:00~13:20", "14:10~14:40", "15:00~15:30", "15:30~15:50"],
                "종목": ["개회식 및 준비운동", "1학년 축구 / 2학년 농구 결승", "2학년 축구 / 3학년 농구 결승", "줄다리기 예선", "3학년 축구 / 1학년 농구 결승", "이벤트 경기 (장애물/줄다리기)", "줄다리기 결승", "계주 예선 및 결승", "시상식 및 폐회식"]
            }
            st.table(pd.DataFrame(schedule_data))

        # 학년별 탭 구성 (반복문 활용해 코드 단축)
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
        # ⚙️ 운영진 전용 결과 입력 창 (실제 DB 연결 전까지 사용)
        # ==========================================
        with st.expander("⚙️ 운영진 전용 결과 입력 (학생들에게는 비밀)"):
            st.warning("이곳에서 승리 팀을 선택하면 전광판과 일반 모드의 점수가 즉시 변동됩니다.")
            for i, m in enumerate(st.session_state.matches):
                # 각 경기마다 승자를 고를 수 있는 라디오 버튼
                winner_choice = st.radio(
                    f"{m['grade']}학년 {m['event']} ({m['time']})",
                    options=["선택 안함", m['team_a'], m['team_b']],
                    index=0 if m['winner'] is None else (1 if m['winner'] == m['team_a'] else 2),
                    key=f"match_{i}"
                )
                
                # 라디오 버튼 선택 시 세션 상태 즉각 업데이트
                new_winner = None if winner_choice == "선택 안함" else winner_choice
                if st.session_state.matches[i]["winner"] != new_winner:
                    st.session_state.matches[i]["winner"] = new_winner
                    st.rerun() # 화면 새로고침하여 즉시 반영
