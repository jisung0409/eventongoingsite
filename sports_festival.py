import streamlit as st
import datetime
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# ==========================================
# 🗄️ DB 통신 함수
# ==========================================
def initialize_data():
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(worksheet="체육대회_경기", ttl="10m")
    
    if 'winner' not in df.columns:
        df['winner'] = None

    matches = []
    relay_data = {
        1: {"1등": None, "2등": None},
        2: {"1등": None, "2등": None},
        3: {"1등": None, "2등": None}
    }
    
    for idx, row in df.iterrows():
        raw_winner = row['winner']
        if pd.isna(raw_winner) or str(raw_winner).strip().lower() in ['nan', 'none', '']:
            clean_winner = None
        else:
            clean_winner = raw_winner

        event_str = str(row['event'])
        if "계주 1등" in event_str:
            relay_data[int(row['grade'])]["1등"] = clean_winner
        elif "계주 2등" in event_str:
            relay_data[int(row['grade'])]["2등"] = clean_winner
        else:
            matches.append({
                "id": row['id'],
                "time": row['time'],
                "grade": int(float(row['grade'])),
                "event": row['event'],
                "team_a": row['team_a'],
                "team_b": row['team_b'],
                "winner": clean_winner,
                "points": row['points']
            })
            
    st.session_state.matches = matches
    st.session_state.relay_data = relay_data

def update_winner_to_db(match_index, new_winner):
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(worksheet="체육대회_경기", ttl=0)
    
    if 'winner' not in df.columns:
        df['winner'] = None
    df['winner'] = df['winner'].astype(object)
    
    match_id = st.session_state.matches[match_index]["id"]
    df.loc[df['id'] == match_id, 'winner'] = "" if new_winner is None else new_winner
    
    conn.update(worksheet="체육대회_경기", data=df)
    st.cache_data.clear()

def update_relay_to_db(grade, rank_type, new_winner):
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(worksheet="체육대회_경기", ttl=0)
    
    if 'winner' not in df.columns:
        df['winner'] = None
    df['winner'] = df['winner'].astype(object)
    
    # [버그 픽스] 학년 데이터를 정수로 강제 통일하여 시트 매칭 오류 방지
    df['grade'] = pd.to_numeric(df['grade'], errors='coerce').fillna(0).astype(int)
    
    event_name = f"계주 {rank_type}"
    condition = (df['grade'] == grade) & (df['event'] == event_name)
    
    if condition.any():
        df.loc[condition, 'winner'] = "" if new_winner is None else new_winner
    else:
        # 시트에 계주 관련 행이 아예 없으면 여기서 알아서 엑셀 줄을 만들어줍니다!
        new_id = int(df['id'].max()) + 1 if not df['id'].empty else 1
        new_row = {
            "id": new_id,
            "time": "15:00",
            "grade": grade,
            "event": event_name,
            "team_a": "전체",
            "team_b": "전체",
            "winner": "" if new_winner is None else new_winner,
            "points": 0
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        
    conn.update(worksheet="체육대회_경기", data=df)
    st.cache_data.clear()

# ==========================================
# 상태 및 우승 종목 수집 로직
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
    team_stats = {}
    
    for m in st.session_state.matches:
        if m["grade"] == grade and m["winner"]:
            w = m["winner"]
            if w not in team_stats:
                team_stats[w] = {"wins": 0, "events": []}
            team_stats[w]["wins"] += 1
            team_stats[w]["events"].append(m["event"]) 
            
    if 'relay_data' in st.session_state and grade in st.session_state.relay_data:
        relay_1st = st.session_state.relay_data[grade].get("1등")
        if relay_1st:
            if relay_1st not in team_stats:
                team_stats[relay_1st] = {"wins": 0, "events": []}
            team_stats[relay_1st]["wins"] += 1
            team_stats[relay_1st]["events"].append("계주 1등")

    return sorted(team_stats.items(), key=lambda x: x[1]["wins"], reverse=True)

# ==========================================
# 전광판 화면 구성 헬퍼 함수
# ==========================================
def display_integrated_kiosk():
    st.markdown("<h1 style='text-align: center; font-size: 3rem; color: #1E90FF; margin-top: -30px; margin-bottom: 20px;'>⚡ 강화고 체육대회 통합 LIVE ⚡</h1>", unsafe_allow_html=True)
    
    col_relay, col_matches = st.columns([1, 2.5])
    
    with col_relay:
        st.markdown("<h3 style='text-align: center; margin-top: 0;'>🏃 계주 결과</h3>", unsafe_allow_html=True)
        for g in [1, 2, 3]:
            r1 = st.session_state.relay_data[g]["1등"]
            r2 = st.session_state.relay_data[g]["2등"]
            if r1 and r2:
                res_html = f"🥇 1등: <b>{r1}</b><br>🥈 2등: <b>{r2}</b>"
            elif r1:
                res_html = f"🥇 1등: <b>{r1}</b><br>🥈 2등: --"
            else:
                res_html = "<span style='color: #888;'>⏳ 결과 대기 중</span>"
            st.markdown(f"<div style='background-color: #f0f2f6; padding: 12px; border-radius: 12px; text-align: center; font-size: 1.1rem; margin-bottom: 15px; border: 2px solid #d1d5db;'>🏅 <b>{g}학년</b><br><div style='margin-top:5px;'>{res_html}</div></div>", unsafe_allow_html=True)
            
    with col_matches:
        st.markdown("<h3 style='text-align: center; margin-top: 0;'>🎯 실시간 매치업 현황</h3>", unsafe_allow_html=True)
        m_cols = st.columns(3)
        for i, m in enumerate(st.session_state.matches):
            status = get_match_status(m["time"], m["winner"])
            with m_cols[i % 3]:
                if "진행 중" in status:
                    st.error(f"**[{m['time']}] {m['grade']}학년 {m['event']}**\n\n### {m['team_a']} VS {m['team_b']}\n\n**{status}**")
                elif "종료" in status:
                    st.success(f"**[{m['time']}] {m['grade']}학년 {m['event']}**\n\n### {status}")
                else:
                    st.info(f"**[{m['time']}] {m['grade']}학년 {m['event']}**\n\n### {m['team_a']} vs {m['team_b']}\n\n{status}")

def display_grade_kiosk(g_idx):
    st.markdown(f"<h1 style='text-align: center; font-size: 4rem; margin-bottom: 20px; margin-top: -20px;'>{g_idx}학년 실시간 전광판</h1>", unsafe_allow_html=True)
    col_rank, col_matches = st.columns([1, 1.2])
    
    with col_rank:
        st.markdown(f"<h3 style='text-align: center; font-size: 2.5rem;'>👑 {g_idx}학년 종합 순위 예측</h3>", unsafe_allow_html=True)
        rankings = calculate_rankings(g_idx)
        if rankings:
            for i, (team, stats) in enumerate(rankings):
                events_str = ", ".join(stats["events"]) 
                
                if i == 0:
                    st.markdown(f"<div style='font-size: 3rem; background: #fffbea; border: 4px solid #FFD700; padding: 20px; border-radius: 15px; margin-bottom: 15px; text-align: center; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);'>🥇 1위: <b>{team}</b><br><span style='font-size:1.5rem; color:#d4af37;'>🏆 {events_str} 우승</span></div>", unsafe_allow_html=True)
                elif i == 1:
                    st.markdown(f"<div style='font-size: 2.5rem; background: #f8f9fa; border: 4px solid #C0C0C0; padding: 15px; border-radius: 15px; margin-bottom: 15px; text-align: center;'>🥈 2위: <b>{team}</b><br><span style='font-size:1.2rem; color:#666;'>🏆 {events_str} 우승</span></div>", unsafe_allow_html=True)
                elif i == 2:
                    st.markdown(f"<div style='font-size: 2rem; background: #fff0f5; border: 4px solid #CD7F32; padding: 15px; border-radius: 15px; margin-bottom: 15px; text-align: center;'>🥉 3위: <b>{team}</b><br><span style='font-size:1rem; color:#666;'>🏆 {events_str} 우승</span></div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div style='font-size: 1.5rem; text-align: center;'>{i+1}위: {team} <span style='font-size:1rem; color:#888;'>({events_str})</span></div>", unsafe_allow_html=True)
        else:
            st.info("아직 승리를 기록한 반이 없습니다.")

    with col_matches:
        st.markdown(f"<h3 style='text-align: center; font-size: 2.5rem;'>🎯 {g_idx}학년 매치업</h3>", unsafe_allow_html=True)
        has_matches = False
        for m in st.session_state.matches:
            if m["grade"] == g_idx:
                has_matches = True
                status = get_match_status(m["time"], m["winner"])
                
                if "진행 중" in status:
                    st.error(f"⏰ **{m['time']} | {m['event']}**\n\n## {m['team_a']} VS {m['team_b']}\n\n**{status}**")
                elif "종료" in status:
                    st.success(f"✅ **{m['time']} | {m['event']}**\n\n## {status}")
                else:
                    st.warning(f"⏳ **{m['time']} | {m['event']}**\n\n## {m['team_a']} vs {m['team_b']}")
        
        if not has_matches:
            st.write("예정된 경기가 없습니다.")

# ==========================================
# 화면 렌더링 메인 함수
# ==========================================
def show_page():
    initialize_data() 
    
    st.markdown("""
        <style>
            [data-testid="stStatusWidget"] {visibility: hidden; height: 0%; position: fixed;}
            .stTable td { font-size: 1rem !important; white-space: nowrap; }
            .stTable th { font-size: 1.1rem !important; background-color: #f0f2f6; }
        </style>
    """, unsafe_allow_html=True)
    
    kiosk_mode = st.toggle("🖥️ 전광판 모드 (전체화면)", value=False)
    
    if kiosk_mode:
        st.markdown("""
            <style>
                [data-testid="stSidebar"] {display: none;}
                .block-container {padding-top: 1rem; padding-bottom: 0rem; max-width: 100%;}
                header {visibility: hidden;}
                .stTabs [data-baseweb='tab-list'] button {font-size: 1.8rem; font-weight: bold;}
            </style>
        """, unsafe_allow_html=True)

        k_tabs = st.tabs(["🌐 통합 현황", "🐣 1학년", "🐥 2학년", "🦅 3학년"])
        with k_tabs[0]:
            display_integrated_kiosk()
        for i in range(1, 4):
            with k_tabs[i]:
                display_grade_kiosk(i)
                
    else:
        st.markdown("<h1 style='text-align: center; color: #1E90FF;'>🏆 2026 강화고 체육대회 🏆</h1>", unsafe_allow_html=True)
        
        tab_all, tab_1, tab_2, tab_3 = st.tabs(["🌐 전체 일정", "🐣 1학년", "🐥 2학년", "🦅 3학년"])

        with tab_all:
            st.markdown("### 📅 체육대회 전체 일정표 (공식)")
            schedule_data = {
                "시간": ["08:40 ~ 09:00", "09:00 ~ 09:50", "09:50 ~ 10:40", "10:40 ~ 11:20", "11:20 ~ 12:10", "12:10 ~ 13:00", "13:00 ~ 13:20", "13:20 ~ 13:50", "13:50 ~ 14:10", "14:10 ~ 14:40", "14:40 ~ 15:00", "15:00 ~ 15:30", "15:30 ~ 15:50", "15:50 ~", "16:00 ~"],
                "종목": ["개회식 및 생활안전교육, 준비운동", "1학년 축구 결승 / 2학년 농구 결승", "2학년 축구 결승 / 3학년 농구 결승", "줄다리기 예선", "3학년 축구 결승 / 1학년 농구 결승", "점심시간 🍱", "이벤트 경기 - 장애물 달리기, 줄다리기", "8자 줄넘기, 2단 뛰기(쌩쌩이)", "이벤트 경기 - 학부모 교직원 줄다리기", "줄다리기 결승", "사제 간 경기 (축구)", "계주 예선, 결승", "성적발표, 시상식 및 폐회식", "정리 및 대청소", "2026학년도 읽걷쓰AI 선언식"],
                "참가대상": ["전교생", "1, 2학년", "2, 3학년", "1, 2, 3학년", "1, 3학년", "1, 2, 3학년", "교직원", "1, 2, 3학년", "학부모, 교직원", "1, 2, 3학년", "교직원 vs 학생회", "1, 2, 3학년", "전교생", "전교생", "희망자"]
            }
            st.table(pd.DataFrame(schedule_data))

        for g_idx, tab in enumerate([tab_1, tab_2, tab_3], start=1):
            with tab:
                st.markdown(f"### 🔥 {g_idx}학년 실시간 경기 현황")
                for m in st.session_state.matches:
                    if m["grade"] == g_idx:
                        status = get_match_status(m["time"], m["winner"])
                        st.write(f"**{m['time']} | {m['event']}** ({m['team_a']} vs {m['team_b']}) ➔ {status}")
                
                st.divider()
                st.markdown(f"#### 👑 {g_idx}학년 종합 순위 예측")
                rankings = calculate_rankings(g_idx)
                if rankings:
                    for i, (team, stats) in enumerate(rankings):
                        events_str = ", ".join(stats["events"])
                        medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉"
                        st.write(f"{medal} **{team}** ➔ 🏆 {events_str} 우승")
                else:
                    st.write("아직 승리를 기록한 반이 없습니다.")

        st.divider()
        
        # ==========================================
        # 🔐 운영진 전용 (Staff Only)
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

                st.subheader("🎯 토너먼트 종목 결과 입력")
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
                        with st.spinner("구글 시트에 저장 중..."):
                            update_winner_to_db(i, new_winner)
                        st.rerun()
                
                st.write("---")
                st.subheader("🏃 학년별 계주 결과 입력")
                class_options = ["선택 안함"] + [f"{i}반" for i in range(1, 9)]
                
                for g in [1, 2, 3]:
                    st.markdown(f"**💡 {g}학년 계주 순위 선택**")
                    current_1st = st.session_state.relay_data[g]["1등"]
                    current_2nd = st.session_state.relay_data[g]["2등"]
                    
                    idx_1st = class_options.index(current_1st) if current_1st in class_options else 0
                    idx_2nd = class_options.index(current_2nd) if current_2nd in class_options else 0
                    
                    c1, c2 = st.columns(2)
                    with c1:
                        sel_1st = st.selectbox(f"{g}학년 계주 1등 반", options=class_options, index=idx_1st, key=f"relay_1st_{g}")
                    with c2:
                        sel_2nd = st.selectbox(f"{g}학년 계주 2등 반", options=class_options, index=idx_2nd, key=f"relay_2nd_{g}")
                        
                    new_1st = None if sel_1st == "선택 안함" else sel_1st
                    new_2nd = None if sel_2nd == "선택 안함" else sel_2nd
                    
                    if current_1st != new_1st:
                        with st.spinner(f"{g}학년 계주 1등 저장 중..."):
                            update_relay_to_db(g, "1등", new_1st)
                        st.rerun()
                        
                    if current_2nd != new_2nd:
                        with st.spinner(f"{g}학년 계주 2등 저장 중..."):
                            update_relay_to_db(g, "2등", new_2nd)
                        st.rerun()
