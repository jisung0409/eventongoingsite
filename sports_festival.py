import streamlit as st
import datetime
import pandas as pd
from streamlit_gsheets import GSheetsConnection # [추가됨] 구글 시트 연결 라이브러리

# ==========================================
# 🗄️ DB 통신 함수 (가장 핵심적인 변경점)
# ==========================================
def initialize_data():
    # 1. 구글 시트에서 데이터 읽어오기
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # ttl=0 옵션: 캐시(임시저장)를 쓰지 않고 항상 실시간으로 가장 최신 데이터를 시트에서 불러옵니다.
    df = conn.read(worksheet="체육대회_경기", ttl=0)
    
    # 엑셀의 빈 칸(NaN)을 파이썬의 None으로 깔끔하게 변환
    df = df.where(pd.notnull(df), None)

    # 2. 읽어온 시트 데이터를 기존 코드(session_state) 형식에 맞게 변환
    matches = []
    for idx, row in df.iterrows():
        matches.append({
            "id": row['id'],
            "time": row['time'],
            "grade": row['grade'],
            "event": row['event'],
            "team_a": row['team_a'],
            "team_b": row['team_b'],
            "winner": row['winner'],
            "points": row['points']
        })
    st.session_state.matches = matches

def update_winner_to_db(match_index, new_winner):
    """관리자가 버튼을 눌렀을 때 구글 시트에 직접 값을 저장하는 함수"""
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(worksheet="체육대회_경기", ttl=0)
    
    # 데이터프레임의 해당 행(match_index), 'winner' 열의 값을 바꿈
    df.at[match_index, 'winner'] = new_winner
    
    # 구글 시트에 변경된 데이터프레임을 덮어쓰기 (저장)
    conn.update(worksheet="체육대회_경기", data=df)
    
    # 캐시를 비워서 다른 접속자들도 즉시 바뀐 화면을 보게 만듦
    st.cache_data.clear()

# ==========================================
# 기존 로직 (상태 계산 등)
# ==========================================
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

# ==========================================
# 화면 UI 그리기
# ==========================================
def show_page():
    # 이제 하드코딩된 데이터가 아니라 구글 시트 데이터를 실시간으로 불러옵니다!
    initialize_data() 
    
    kiosk_mode = st.toggle("🖥️ 전광판 모드 (전체화면)", value=False)
    
    if kiosk_mode:
        # [전광판 모드 UI - 기존과 100% 동일]
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
        # [일반(모바일) 모드 UI - 기존과 100% 동일]
        st.markdown("<h1 style='text-align: center; color: #1E90FF;'>🏆 2026 강화고 체육대회 🏆</h1>", unsafe_allow_html=True)
        
        tab_all, tab_1, tab_2, tab_3 = st.tabs(["🌐 전체 일정", "🐣 1학년", "🐥 2학년", "🦅 3학년"])

        with tab_all:
            st.markdown("### 📅 체육대회 전체 일정표 (공식)")
            schedule_data = {
                "시간": ["08:40 ~ 09:00", "09:00 ~ 09:50", "09:50 ~ 10:40", "10:40 ~ 11:20", "11:20 ~ 12:10", "12:10 ~ 13:00", "13:00 ~ 13:20", "13:20 ~ 13:50", "13:50 ~ 14:10", "14:10 ~ 14:40", "14:40 ~ 15:00", "15:00 ~ 15:30", "15:30 ~ 15:50", "15:50 ~", "16:00 ~"],
                "종목": ["개회식 및 생활안전교육, 준비운동", "1학년 축구 결승 / 2학년 농구 결승", "2학년 축구 결승 / 3학년 농구 결승", "줄다리기 예선", "3학년 축구 결승 / 1학년 농구 결승", "점심시간 🍱", "이벤트 경기 - 장애물 달리기, 줄다리기", "8자 줄넘기, 2단 뛰기(쌩쌩이)", "이벤트 경기 - 학부모 교직원 줄다리기", "줄다리기 결승", "사제 간 경기 (축구)", "계주 예선, 결승", "성적발표, 시상식 및 폐회식", "정리 및 대청소", "2026학년도 읽걷쓰AI 선언식"],
                "참가대상": ["전교생", "1, 2학년", "2, 3학년", "1, 2, 3학년", "1, 3학년", "1, 2, 3학년", "교직원", "1, 2, 3학년", "학부모, 교직원", "1, 2, 3학년", "교직원 vs 학생회", "1, 2, 3학년", "전교생", "전교생", "희망자"]
            }
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
        # 🔐 운영진 전용 (여기가 DB 쓰기 핵심입니다!)
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

                st.warning("이곳에서 승리 팀을 선택하면 전광판이 바뀌고, 구글 시트에도 영구 저장됩니다.")
                
                for i, m in enumerate(st.session_state.matches):
                    winner_choice = st.radio(
                        f"{m['grade']}학년 {m['event']} ({m['time']})",
                        options=["선택 안함", m['team_a'], m['team_b']],
                        index=0 if m['winner'] is None else (1 if m['winner'] == m['team_a'] else 2),
                        key=f"match_{i}"
                    )
                    
                    new_winner = None if winner_choice == "선택 안함" else winner_choice
                    
                    # [변경점] 관리자가 새로운 승리팀을 클릭한 순간!
                    if st.session_state.matches[i]["winner"] != new_winner:
                        # 1. 화면 업데이트를 위해 세션 상태 변경
                        st.session_state.matches[i]["winner"] = new_winner
                        
                        # 2. "진짜" 데이터베이스(구글 시트)에 값을 덮어쓰기
                        with st.spinner("구글 시트에 저장 중입니다..."):
                            update_winner_to_db(i, new_winner)
                        
                        # 3. 화면 새로고침
                        st.rerun()
