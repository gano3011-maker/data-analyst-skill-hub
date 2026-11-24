import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Data Analyst Skill Hub", page_icon="🚀", layout="wide")

# ตกแต่ง UI เพิ่มสีสันด้วย CSS
st.markdown("""
<style>
    .hero-box {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #ec4899 100%);
        padding: 24px 28px;
        border-radius: 16px;
        color: white;
        margin-bottom: 20px;
    }
    .hero-title { font-size: 2rem; font-weight: 800; margin: 0; }
    .hero-sub { font-size: 0.95rem; opacity: 0.9; margin-top: 6px; }
    .rank-badge {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        padding: 6px 14px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 0.9rem;
        margin-top: 12px;
    }
    .flashcard {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        color: white;
        padding: 36px 24px;
        border-radius: 18px;
        text-align: center;
        border: 2px solid #6366f1;
        margin: 12px 0;
    }
    .mission-card {
        background: #f8fafc;
        border-left: 6px solid #7c3aed;
        padding: 18px 20px;
        border-radius: 12px;
        color: #1e293b;
    }
</style>
""", unsafe_allow_html=True)

FILE_PATH = "skills.csv"

def load_data():
    return pd.read_csv(FILE_PATH)

def save_data(df):
    try:
        df.to_csv(FILE_PATH, index=False)
    except Exception:
        pass  # กรณีรันบน Cloud บางจังหวะ เก็บไว้ใน session_state ต่อได้

# เก็บข้อมูลใน session_state เพื่อให้อัปเดตลื่นไหลทุกแท็บ
if "df" not in st.session_state:
    st.session_state.df = load_data()

df = st.session_state.df

# คำนวณ XP และ Rank
mastered = len(df[df["Status"] == "ใช้คล่องแล้ว"])
learning = len(df[df["Status"] == "กำลังเรียน"])
total_skills = len(df)
xp = (mastered * 15) + (learning * 5)
max_xp = total_skills * 15
progress_pct = int((mastered / total_skills) * 100) if total_skills > 0 else 0

def get_rank(points):
    if points >= 1400: return "👑 Lv.5 Data Master"
    if points >= 900:  return "🧙‍♂️ Lv.4 Analytics Wizard"
    if points >= 450:  return "⚡ Lv.3 Query Explorer"
    if points >= 150:  return "🛠️ Lv.2 Data Apprentice"
    return "🌱 Lv.1 Data Rookie"

# Header Banner
st.markdown(f"""
<div class="hero-box">
    <div class="hero-title">🚀 Personal Data Analyst Skill Hub</div>
    <div class="hero-sub">อัปสกิล 4 เครื่องมือหลักสาย Data: Excel • SQL • Power BI DAX • Python (Pandas)</div>
    <div class="rank-badge">{get_rank(xp)} &nbsp;|&nbsp; ⭐ {xp:,} / {max_xp:,} XP</div>
</div>
""", unsafe_allow_html=True)

# แถบ Metrics ภาพรวม
c1, c2, c3, c4 = st.columns(4)
c1.metric("📚 ฟังก์ชันทั้งหมด", f"{total_skills} ตัว")
c2.metric("✅ ใช้คล่องแล้ว", f"{mastered} ตัว")
c3.metric("⏳ กำลังเรียน", f"{learning} ตัว")
c4.metric("🎯 ความคืบหน้า", f"{progress_pct}%")
st.progress(progress_pct / 100)

# สร้าง 5 แท็บหลัก
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 ภาพรวม & ภารกิจวันนี้",
    "🃏 Flashcards ทบทวน",
    "🎮 มินิเกมทายฟังก์ชัน",
    "🔀 เทียบสูตร 4 เครื่องมือ",
    "📚 คลัง 120 ฟังก์ชัน"
])

# ==========================================
# TAB 1: DASHBOARD & DAILY MISSION
# ==========================================
with tab1:
    col_left, col_right = st.columns([1.3, 1])

    with col_left:
        st.subheader("📈 ความคืบหน้าแยกตามเครื่องมือ")
        cat_summary = []
        for cat in df["Category"].unique():
            sub = df[df["Category"] == cat]
            done = len(sub[sub["Status"] == "ใช้คล่องแล้ว"])
            in_prog = len(sub[sub["Status"] == "กำลังเรียน"])
            not_start = len(sub[sub["Status"] == "ยังไม่เริ่ม"])
            pct = int((done / len(sub)) * 100) if len(sub) > 0 else 0
            st.write(f"**{cat}** — คล่องแล้ว {done}/{len(sub)} ตัว ({pct}%)")
            st.progress(pct / 100)
            cat_summary.append({
                "เครื่องมือ": cat,
                "ใช้คล่องแล้ว": done,
                "กำลังเรียน": in_prog,
                "ยังไม่เริ่ม": not_start
            })

        chart_df = pd.DataFrame(cat_summary).set_index("เครื่องมือ")
        st.bar_chart(chart_df[["ใช้คล่องแล้ว", "กำลังเรียน"]])

    with col_right:
        st.subheader("🎯 ภารกิจประจำวัน (Daily Mission)")
        unmastered = df[df["Status"] != "ใช้คล่องแล้ว"]

        if len(unmastered) == 0:
            st.success("🎉 สุดยอด! คุณเก็บครบทั้ง 120 ฟังก์ชันแล้ว!")
        else:
            if "mission_idx" not in st.session_state or st.session_state.mission_idx not in unmastered.index:
                st.session_state.mission_idx = random.choice(unmastered.index.tolist())

            m_row = df.loc[st.session_state.mission_idx]
            st.markdown(f"""
            <div class="mission-card">
                <div style="font-size:0.85rem; color:#6d28d9; font-weight:700;">หมวด: {m_row['Category']}</div>
                <div style="font-size:1.6rem; font-weight:800; margin:6px 0;">{m_row['Function']}</div>
                <div style="font-size:0.95rem; margin-bottom:10px;">{m_row['Description']}</div>
                <div style="background:#1e293b; color:#38bdf8; padding:10px 12px; border-radius:8px; font-family:monospace; font-size:0.85rem;">
                    {m_row['Example']}
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.write("")
            b1, b2, b3 = st.columns(3)
            if b1.button("🎲 สุ่มภารกิจใหม่", use_container_width=True):
                st.session_state.mission_idx = random.choice(unmastered.index.tolist())
                st.rerun()
            if b2.button("⏳ กำลังเรียน (+5 XP)", use_container_width=True):
                st.session_state.df.at[st.session_state.mission_idx, "Status"] = "กำลังเรียน"
                save_data(st.session_state.df)
                st.rerun()
            if b3.button("✅ คล่องแล้ว (+15 XP)", type="primary", use_container_width=True):
                st.session_state.df.at[st.session_state.mission_idx, "Status"] = "ใช้คล่องแล้ว"
                save_data(st.session_state.df)
                st.balloons()
                st.session_state.mission_idx = random.choice(df.index.tolist())
                st.rerun()

# ==========================================
# TAB 2: FLASHCARDS
# ==========================================
with tab2:
    st.subheader("🃏 การ์ดทบทวนความจำ (Flashcards)")
    fc_cat = st.selectbox("เลือกหมวดที่อยากทบทวน:", ["ทั้งหมด"] + list(df["Category"].unique()))
    fc_pool = df if fc_cat == "ทั้งหมด" else df[df["Category"] == fc_cat]

    if "fc_idx" not in st.session_state or st.session_state.fc_idx not in fc_pool.index:
        st.session_state.fc_idx = random.choice(fc_pool.index.tolist())
        st.session_state.fc_flip = False

    card = df.loc[st.session_state.fc_idx]

    st.markdown(f"""
    <div class="flashcard">
        <div style="font-size:0.9rem; color:#a5b4fc; margin-bottom:8px;">{card['Category']} • สถานะ: {card['Status']}</div>
        <div style="font-size:2.2rem; font-weight:800; color:#f8fafc;">{card['Function']}</div>
        {"<hr style='border-color:#475569; margin:18px 0;'><div style='font-size:1.1rem; color:#e2e8f0;'>" + str(card['Description']) + "</div><div style='margin-top:14px; background:#0f172a; padding:12px; border-radius:10px; font-family:monospace; color:#34d399;'>" + str(card['Example']) + "</div>" if st.session_state.fc_flip else "<div style='margin-top:16px; color:#94a3b8; font-size:0.95rem;'>นึกในใจก่อนว่าฟังก์ชันนี้ใช้ทำอะไร แล้วกดปุ่มเฉลยด้านล่าง 👇</div>"}
    </div>
    """, unsafe_allow_html=True)

    fc1, fc2, fc3 = st.columns(3)
    if fc1.button("🔄 พลิกการ์ดดูเฉลย / ซ่อน", use_container_width=True):
        st.session_state.fc_flip = not st.session_state.fc_flip
        st.rerun()
    if fc2.button("✅ จำแม่นแล้ว! (เปลี่ยนเป็นคล่องแล้ว)", type="primary", use_container_width=True):
        st.session_state.df.at[st.session_state.fc_idx, "Status"] = "ใช้คล่องแล้ว"
        save_data(st.session_state.df)
        st.session_state.fc_idx = random.choice(fc_pool.index.tolist())
        st.session_state.fc_flip = False
        st.rerun()
    if fc3.button("➡️ สุ่มใบถัดไป", use_container_width=True):
        st.session_state.fc_idx = random.choice(fc_pool.index.tolist())
        st.session_state.fc_flip = False
        st.rerun()

# ==========================================
# TAB 3: MINI QUIZ GAME
# ==========================================
with tab3:
    st.subheader("🎮 มินิเกมทายฟังก์ชันสาย Data")

    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = 0
        st.session_state.quiz_total = 0
        st.session_state.quiz_streak = 0

    def new_question():
        target = df.sample(1).iloc[0]
        same_cat = df[(df["Category"] == target["Category"]) & (df["Function"] != target["Function"])]
        wrong_choices = same_cat.sample(min(3, len(same_cat)))["Function"].tolist()
        options = wrong_choices + [target["Function"]]
        random.shuffle(options)
        st.session_state.q_target = target.to_dict()
        st.session_state.q_options = options
        st.session_state.q_answered = False
        st.session_state.q_result = ""

    if "q_target" not in st.session_state:
        new_question()

    qs1, qs2, qs3 = st.columns(3)
    qs1.metric("🏆 คะแนนสะสม", f"{st.session_state.quiz_score} / {st.session_state.quiz_total}")
    qs2.metric("🔥 คอมโบต่อเนื่อง", f"{st.session_state.quiz_streak} ข้อติด")
    if qs3.button("🔄 รีเซ็ตคะแนน", use_container_width=True):
        st.session_state.quiz_score = 0
        st.session_state.quiz_total = 0
        st.session_state.quiz_streak = 0
        new_question()
        st.rerun()

    q = st.session_state.q_target
    st.info(f"**หมวด {q['Category']}** — ฟังก์ชันใดมีหน้าที่ดังนี้?\n\n### \"{q['Description']}\"")

    choice = st.radio("เลือกคำตอบของคุณ:", st.session_state.q_options, index=None, disabled=st.session_state.q_answered)

    qb1, qb2 = st.columns(2)
    if qb1.button("✔️ ส่งคำตอบ", type="primary", disabled=st.session_state.q_answered or choice is None, use_container_width=True):
        st.session_state.quiz_total += 1
        st.session_state.q_answered = True
        if choice == q["Function"]:
            st.session_state.quiz_score += 1
            st.session_state.quiz_streak += 1
            st.session_state.q_result = "correct"
            if st.session_state.quiz_streak % 3 == 0:
                st.balloons()
        else:
            st.session_state.quiz_streak = 0
            st.session_state.q_result = "wrong"
        st.rerun()

    if qb2.button("➡️ ข้อถัดไป", use_container_width=True):
        new_question()
        st.rerun()

    if st.session_state.q_answered:
        if st.session_state.q_result == "correct":
            st.success(f"🎉 ถูกต้อง! คำตอบคือ **{q['Function']}**\n\nตัวอย่าง: `{q['Example']}`")
        else:
            st.error(f"❌ ยังไม่ถูกครับ คำตอบที่ถูกต้องคือ **{q['Function']}**\n\nตัวอย่าง: `{q['Example']}`")

# ==========================================
# TAB 4: CROSS-TOOL TRANSLATOR
# ==========================================
with tab4:
    st.subheader("🔀 เทียบสูตรข้าม 4 เครื่องมือ (ทำงานเดียวกัน เขียนต่างกันยังไง?)")
    st.caption("ช่วยให้จำเชื่อมโยงได้เร็วขึ้นเวลาต้องย้ายงานจาก Excel ไปทำใน SQL, Power BI หรือ Python")

    compare_data = [
        {"งานที่ต้องการทำ": "หาผลรวมทั้งหมด", "Excel": "=SUM(A:A)", "SQL": "SELECT SUM(col)", "Power BI DAX": "SUM(Table[Col])", "Python (Pandas)": "df['col'].sum()"},
        {"งานที่ต้องการทำ": "กรองข้อมูลตามเงื่อนไข", "Excel": "COUNTIFS / SUMIFS", "SQL": "WHERE ...", "Power BI DAX": "CALCULATE(..., FILTER())", "Python (Pandas)": "df[df['col'] > 100]"},
        {"งานที่ต้องการทำ": "เชื่อม 2 ตารางเข้าด้วยกัน", "Excel": "VLOOKUP / XLOOKUP", "SQL": "LEFT JOIN / INNER JOIN", "Power BI DAX": "RELATED()", "Python (Pandas)": "pd.merge(df1, df2)"},
        {"งานที่ต้องการทำ": "จัดกลุ่มเพื่อสรุปยอด", "Excel": "Pivot Table / SUMIF", "SQL": "GROUP BY", "Power BI DAX": "SUMMARIZE / ALLEXCEPT", "Python (Pandas)": "df.groupby('col').sum()"},
        {"งานที่ต้องการทำ": "เงื่อนไข ใช่ / ไม่ใช่", "Excel": "=IF(cond, T, F)", "SQL": "CASE WHEN ... END", "Power BI DAX": "IF() / SWITCH()", "Python (Pandas)": "df.apply(lambda x: ...)"},
        {"งานที่ต้องการทำ": "หาค่าที่ไม่ซ้ำกัน", "Excel": "UNIQUE()", "SQL": "SELECT DISTINCT", "Power BI DAX": "DISTINCT() / VALUES()", "Python (Pandas)": "df['col'].unique()"},
        {"งานที่ต้องการทำ": "เรียงลำดับมากไปน้อย", "Excel": "Sort (Z to A)", "SQL": "ORDER BY col DESC", "Power BI DAX": "TOPN() / RANKX()", "Python (Pandas)": "df.sort_values(ascending=False)"},
        {"งานที่ต้องการทำ": "จัดการค่าว่าง (Null/Blank)", "Excel": "IFERROR / ISBLANK", "SQL": "COALESCE(col, 0)", "Power BI DAX": "ISBLANK()", "Python (Pandas)": "fillna(0) / dropna()"},
    ]
    st.dataframe(pd.DataFrame(compare_data), use_container_width=True, hide_index=True)

# ==========================================
# TAB 5: FULL 120 SKILLS TRACKER
# ==========================================
with tab5:
    st.subheader("📚 คลัง 120 ฟังก์ชัน (ค้นหาและอัปเดตสถานะ)")
    f1, f2, f3 = st.columns([1.2, 1.2, 1.5])
    selected_cat = f1.multiselect("เลือกเครื่องมือ:", options=df["Category"].unique(), default=df["Category"].unique())
    selected_status = f2.multiselect("สถานะ:", options=["ยังไม่เริ่ม", "กำลังเรียน", "ใช้คล่องแล้ว"], default=["ยังไม่เริ่ม", "กำลังเรียน", "ใช้คล่องแล้ว"])
    search_query = f3.text_input("🔍 ค้นหาชื่อฟังก์ชัน / คำอธิบาย:")

    filtered_df = df[(df["Category"].isin(selected_cat)) & (df["Status"].isin(selected_status))]
    if search_query:
        filtered_df = filtered_df[
            filtered_df["Function"].str.contains(search_query, case=False, na=False) |
            filtered_df["Description"].str.contains(search_query, case=False, na=False)
        ]

    st.caption(f"แสดงทั้งหมด {len(filtered_df)} จาก {len(df)} รายการ (ดับเบิลคลิกที่ช่อง 'สถานะ' เพื่อเปลี่ยน)")
    edited_df = st.data_editor(
        filtered_df,
        column_config={
            "Status": st.column_config.SelectboxColumn(
                "สถานะ",
                options=["ยังไม่เริ่ม", "กำลังเรียน", "ใช้คล่องแล้ว"],
                required=True,
            ),
            "Example": st.column_config.TextColumn("ตัวอย่างการใช้งาน", width="large"),
        },
        disabled=["Category", "Function", "Description"],
        hide_index=True,
        use_container_width=True,
        height=450,
    )

    if st.button("💾 บันทึกความคืบหน้า", type="primary"):
        st.session_state.df.update(edited_df)
        save_data(st.session_state.df)
        st.success("บันทึกสถานะและอัปเดต XP เรียบร้อยแล้ว!")
        st.rerun()
