import streamlit as st
import datetime
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# ==========================================
# 🗄️ DB 통신 함수 (초기 접속 방어 & 일괄 업데이트)
# ==========================================
def initialize_data():
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    try:
        df = conn.read(worksheet="체육대회_경기", ttl="0")
    except Exception:
        st.warning("⚠️ 현재 접속자가 많아 구글 서버와 통신이 지연되고 있습니다. 약 1분 뒤에 새로고침(F5) 해주세요.")
        st.stop()
    
    if 'winner' not in df.columns:
        df['winner'] = None

    matches = []
    extra_events = {
        1: {"계주 1등": None, "계주 2등": None, "줄다리기 1등": None, "8자 줄넘기 1등": None, "쌩쌩이 줄넘기 1등": None},
        2: {"계주 1등": None, "계주 2등": None, "줄다리기 1등": None, "8자 줄넘기 1등": None, "쌩쌩이 줄넘기 1등": None},
        3: {"계주 1등": None, "계주 2등": None, "줄다리기 1등": None, "8자 줄넘기 1등": None, "쌩쌩이 줄넘기 1등": None}
    }
    
    for idx, row in df.iterrows():
        raw_winner = row['winner']
        if pd.isna(raw_winner) or str(raw_winner).strip().lower() in ['nan', 'none', '']:
            clean_winner = None
        else:
            clean_winner = raw_winner

        event_str = str(row['event']).strip()
        
        try:
            grade_val = int(float(row['grade']))
        except (ValueError, TypeError):
            grade_val = 0
        
        if event_str in ["계주 1등", "계주 2등", "줄다리기 1등", "8자 줄넘기 1등", "쌩쌩이 줄넘기 1등"] and grade_val in [1, 2, 3]:
            extra_events[grade_val][event_str] = clean_winner
        else:
            if "줄다리기" in event_str and grade_val == 3 and row['id'] == 7:
                continue
                
            # [추가됨] 참가팀이 "전체"인 기록제 종목은 매치업 전광판 리스트에서 숨김 처리!
            if str(row['team_a']).strip() == "전체":
                continue
                
            matches.append({
                "id": row['id'],
                "time": row['time'],
                "grade": grade_val,
                "event": row['event'],
                "team_a": row['team_a'],
                "team_b": row['team_b'],
                "winner": clean_winner,
                "points": row['points']
            })
            
    st.session_state.matches = matches
    st.session_state.extra_events = extra_events

def bulk_update_db(match_changes, extra_changes):
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(worksheet="체육대회_경기", ttl=0)
    
    if 'winner' not in df.columns:
        df['winner'] = None
    df['winner'] = df['winner'].astype(object)
    df['grade'] = pd.to_numeric(df['grade'], errors='coerce').fillna(0).astype(int)
    
    for match_id, new_winner in match_changes.items():
        df.loc[df['id'] == match_id, 'winner'] = "" if new_winner is None else new_winner
        
    for (grade, event_name), new_winner in extra_changes.items():
        condition = (df['grade'] == grade) & (df['event'] == event_name)
        if condition.any():
            df.loc[condition, 'winner'] = "" if new_winner is None else new_winner
        else:
            new_id = int(df['id'].max()) + 1 if not df['id'].empty else 1
            new_row = {
                "id": new_id, "time": "15:00", "grade": grade, "event": event_name,
                "team_a": "전체", "team_b": "전체", "winner": "" if new_winner is None else new_winner,
                "points": 0
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            
    conn.update(worksheet="체육대회_경기", data=df)
    st.cache_data.clear()

# ==========================================
# 상태 및 성적 수집 로직
# ==========================================
def get_match_status(match_time_str, winner):
    # [수정됨] 서버 위치 상관없이 무조건 한국 시간(KST)으로 고정
    KST = datetime.timezone(datetime.timedelta(hours=9))
    now = datetime.datetime.now(KST).strftime("%H:%M")
    
    # [수정됨] 9:00 처럼 적힌 시간을 09:00 으로 강제 변환하여 문자열 비교 오류 방지
    match_time_str = str(match_time_str).strip()
    if len(match_time_str) == 4 and match_time_str[1] == ":":
        match_time_str = "0" + match_time_str

    if winner:
        return f"✅ 종료 ({winner} 승리)"
    elif now >= match_time_str:
        return "⏳ 예정"
    else:
        return "⏳ 예정"

def calculate_rankings(grade):
    team_stats = {}
    
    def add_achievement(team, record_text, is_win=True):
        if team not in team_stats:
            team_stats[team] = {"wins": 0, "achievements": []}
        if is_win:
            team_stats[team]["wins"] += 1
        team_stats[team]["achievements"].append(record_text)

    for m in st.session_state.matches:
        if m["grade"] == grade and m["winner"]:
            add_achievement(m["winner"], f"{m['event']} 우승", is_win=True)
            
    if 'extra_events' in st.session_state and grade in st.session_state.extra_events:
        events = st.session_state.extra_events[grade]
        if events.get("계주 1등"): add_achievement(events["계주 1등"], "계주 1등", is_win=True)
        if events.get("계주 2등"): add_achievement(events["계주 2등"], "계주 2등", is_win=False)
        if events.get("줄다리기 1등"): add_achievement(events["줄다리기 1등"], "줄다리기 1등", is_win=True)
        if events.get("8자 줄넘기 1등"): add_achievement(events["8자 줄넘기 1등"], "8자 줄넘기 1등", is_win=True)
        if events.get("쌩쌩이 줄넘기 1등"): add_achievement(events["쌩쌩이 줄넘기 1등"], "쌩쌩이 1등", is_win=True)

    return sorted(team_stats.items(), key=lambda x: x[1]["wins"], reverse=True)

# ==========================================
# 전광판 화면 구성 헬퍼 함수
# ==========================================
def display_integrated_kiosk():
    st.markdown("<h1 style='text-align: center; font-size: 3rem; color: #1E90FF; margin-top: -30px; margin-bottom: 20px;'>⚡ 강화고 체육대회 통합 LIVE ⚡</h1>", unsafe_allow_html=True)
    
    col_relay, col_matches = st.columns([1.2, 2.3])
    with col_relay:
        st.markdown("<h3 style='text-align: center; margin-top: 0;'>📊 학년별 주요 기록</h3>", unsafe_allow_html=True)
        for g in [1, 2, 3]:
            # 1, 2학년 미저장 안내
            if g in [1, 2]:
                content_html = "<div style='text-align: center; padding: 15px 0; color: #888; font-size: 0.95rem;'>해당 학년의 체육대회 결과는<br>저장되지 않았습니다.</div>"
                st.markdown(f"<div style='background-color: #f0f2f6; padding: 12px; border-radius: 12px; font-size: 1rem; margin-bottom: 12px; border: 2px solid #d1d5db;'>🏅 <b style='font-size:1.1rem;'>{g}학년 종합 결과</b><br>{content_html}</div>", unsafe_allow_html=True)
            else:
                events = st.session_state.extra_events[g]
                lines = []
                if events["계주 1등"] or events["계주 2등"]:
                    r1 = events["계주 1등"] if events["계주 1등"] else "--"
                    r2 = events["계주 2등"] if events["계주 2등"] else "--"
                    lines.append(f"🏃 계주 ➔ 1등: <b>{r1}</b> / 2등: <b>{r2}</b>")
                else:
                    lines.append("🏃 계주 ➔ <span style='color:#888;'>결과 대기 중</span>")
                    
                lines.append(f" rope 8자 ➔ <b>{events['8자 줄넘기 1등'] if events['8자 줄넘기 1등'] else '--'}</b>")
                lines.append(f"⏱️ 쌩쌩이 ➔ <b>{events['쌩쌩이 줄넘기 1등'] if events['쌩쌩이 줄넘기 1등'] else '--'}</b>")
                lines.append(f"💪 줄다리기 ➔ <b>{events['줄다리기 1등'] if events['줄다리기 1등'] else '--'}</b>")
                
                content_html = "<br>".join(lines)
                st.markdown(f"<div style='background-color: #f0f2f6; padding: 12px; border-radius: 12px; font-size: 1rem; margin-bottom: 12px; border: 2px solid #d1d5db;'>🏅 <b style='font-size:1.1rem;'>{g}학년 종합 결과</b><br><div style='margin-top:8px; line-height: 1.6;'>{content_html}</div></div>", unsafe_allow_html=True)
            
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
    col_rank, col_matches = st.columns([1.1, 1.1])
    
    with col_rank:
        st.markdown(f"<h3 style='text-align: center; font-size: 2.5rem;'>👑 {g_idx}학년 종합 순위 예측</h3>", unsafe_allow_html=True)
        
        # 1, 2학년 미저장 안내
        if g_idx in [1, 2]:
            st.info("해당 학년의 체육대회 결과는 저장되지 않았습니다.")
        else:
            rankings = calculate_rankings(g_idx)
            if rankings:
                for i, (team, stats) in enumerate(rankings):
                    achievements_str = ", ".join(stats["achievements"])
                    if i == 0:
                        st.markdown(f"<div style='font-size: 2.8rem; background: #fffbea; border: 4px solid #FFD700; padding: 18px; border-radius: 15px; margin-bottom: 15px; text-align: center; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);'>🥇 1위: <b>{team}</b><br><span style='font-size:1.4rem; color:#d4af37;'>🏆 {achievements_str}</span></div>", unsafe_allow_html=True)
                    elif i == 1:
                        st.markdown(f"<div style='font-size: 2.3rem; background: #f8f9fa; border: 4px solid #C0C0C0; padding: 14px; border-radius: 15px; margin-bottom: 15px; text-align: center;'>🥈 2위: <b>{team}</b><br><span style='font-size:1.2rem; color:#666;'>🏆 {achievements_str}</span></div>", unsafe_allow_html=True)
                    elif i == 2:
                        st.markdown(f"<div style='font-size: 1.9rem; background: #fff0f5; border: 4px solid #CD7F32; padding: 14px; border-radius: 15px; margin-bottom: 15px; text-align: center;'>🥉 3위: <b>{team}</b><br><span style='font-size:1rem; color:#666;'>🏆 {achievements_str}</span></div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div style='font-size: 1.4rem; text-align: center; margin-bottom: 10px;'>{i+1}위: {team} <span style='font-size:0.95rem; color:#888;'>({achievements_str})</span></div>", unsafe_allow_html=True)
            else:
                st.info("아직 성적을 기록한 반이 없습니다.")

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
                
                # 1, 2학년 미저장 안내
                if g_idx in [1, 2]:
                    st.info("해당 학년의 체육대회 결과는 저장되지 않았습니다.")
                else:
                    rankings = calculate_rankings(g_idx)
                    if rankings:
                        for i, (team, stats) in enumerate(rankings):
                            achievements_str = ", ".join(stats["achievements"])
                            medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉"
                            st.write(f"{medal} **{team}** ➔ 🏆 {achievements_str}")
                    else:
                        st.write("아직 성적을 기록한 반이 없습니다.")

        st.divider()
        
        # ==========================================
        # 🔐 운영진 전용 (일괄 저장 폼 도입)
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

                st.info("💡 **운영 꿀팁:** 경기가 하나 끝날 때마다 결과를 선택하고, 맨 아래의 **[💾 실시간 결과 전광판에 반영하기]** 버튼을 누르시면 됩니다!")
                
                with st.form("admin_bulk_update_form"):
                    
                    st.subheader("🎯 토너먼트 종목 결과 입력")
                    match_inputs = []
                    for i, m in enumerate(st.session_state.matches):
                        val = st.radio(
                            f"{m['grade']}학년 {m['event']} ({m['time']})",
                            options=["선택 안함", m['team_a'], m['team_b']],
                            index=0 if m['winner'] is None else (1 if m['winner'] == m['team_a'] else 2)
                        )
                        match_inputs.append({"id": m['id'], "val": val})
                    
                    st.write("---")
                    st.subheader("📊 학년별 점수제/기록제 종목 결과 입력")
                    extra_inputs = []
                    class_options = ["선택 안함"] + [f"{i}반" for i in range(1, 9)]
                    
                    for g in [1, 2, 3]:
                        st.markdown(f"#### 💡 **{g}학년 세부 기록 설정**")
                        current_events = st.session_state.extra_events[g]
                        
                        c1, c2 = st.columns(2)
                        idx_1st = class_options.index(current_events["계주 1등"]) if current_events["계주 1등"] in class_options else 0
                        idx_2nd = class_options.index(current_events["계주 2등"]) if current_events["계주 2등"] in class_options else 0
                        v_relay1 = c1.selectbox(f"{g}학년 계주 1등", options=class_options, index=idx_1st)
                        v_relay2 = c2.selectbox(f"{g}학년 계주 2등", options=class_options, index=idx_2nd)
                        extra_inputs.append({"grade": g, "event": "계주 1등", "val": v_relay1})
                        extra_inputs.append({"grade": g, "event": "계주 2등", "val": v_relay2})
                            
                        c3, c4, c5 = st.columns(3)
                        idx_tug = class_options.index(current_events["줄다리기 1등"]) if current_events["줄다리기 1등"] in class_options else 0
                        idx_rope8 = class_options.index(current_events["8자 줄넘기 1등"]) if current_events["8자 줄넘기 1등"] in class_options else 0
                        idx_ropesg = class_options.index(current_events["쌩쌩이 줄넘기 1등"]) if current_events["쌩쌩이 줄넘기 1등"] in class_options else 0
                        v_tug = c3.selectbox(f"{g}학년 줄다리기 1등", options=class_options, index=idx_tug)
                        v_rope8 = c4.selectbox(f"{g}학년 8자 줄넘기 1등", options=class_options, index=idx_rope8)
                        v_ropesg = c5.selectbox(f"{g}학년 쌩쌩이 줄넘기 1등", options=class_options, index=idx_ropesg)
                        extra_inputs.append({"grade": g, "event": "줄다리기 1등", "val": v_tug})
                        extra_inputs.append({"grade": g, "event": "8자 줄넘기 1등", "val": v_rope8})
                        extra_inputs.append({"grade": g, "event": "쌩쌩이 줄넘기 1등", "val": v_ropesg})
                        st.write("")

                    submitted = st.form_submit_button("💾 방금 선택한 결과 전광판에 즉시 반영하기", use_container_width=True)
                    
                    if submitted:
                        final_matches = {}
                        for mi in match_inputs:
                            final_matches[mi["id"]] = None if mi["val"] == "선택 안함" else mi["val"]
                            
                        final_extras = {}
                        for ei in extra_inputs:
                            final_extras[(ei["grade"], ei["event"])] = None if ei["val"] == "선택 안함" else ei["val"]
                            
                        try:
                            with st.spinner("구글 시트에 안전하게 기록 중입니다..."):
                                bulk_update_db(final_matches, final_extras)
                            st.success("✅ 전광판 업데이트 완료! 현장에 바로 반영되었습니다.")
                            st.rerun()
                        except Exception as e:
                            st.error(f"⚠️ 구글 서버 통신 오류! 잠시 후 버튼을 다시 눌러주세요. (상세: {e})")
