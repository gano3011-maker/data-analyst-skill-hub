import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Data Analyst Skill Hub", page_icon="🎮", layout="wide")

# ==========================================
# CUSTOM CSS ANIMATIONS & GAME UI
# ==========================================
st.markdown("""
<style>
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    @keyframes floatCard {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-6px); }
    }
    @keyframes pulseGlow {
        0%, 100% { box-shadow: 0 0 15px rgba(99, 102, 241, 0.4); }
        50% { box-shadow: 0 0 28px rgba(236, 72, 153, 0.75); }
    }
    @keyframes popIn {
        0% { transform: scale(0.92); opacity: 0; }
        100% { transform: scale(1); opacity: 1; }
    }

    .hero-box {
        background: linear-gradient(-45deg, #4f46e5, #7c3aed, #ec4899, #06b6d4);
        background-size: 300% 300%;
        animation: gradientBG 8s ease infinite;
        padding: 26px 30px;
        border-radius: 20px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px rgba(79, 70, 229, 0.25);
    }
    .hero-title { font-size: 2.1rem; font-weight: 800; margin: 0; letter-spacing: -0.5px; }
    .hero-sub { font-size: 0.95rem; opacity: 0.92; margin-top: 6px; }
    .rank-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.22);
        backdrop-filter: blur(8px);
        padding: 7px 16px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 0.95rem;
        margin-top: 14px;
        border: 1px solid rgba(255,255,255,0.35);
    }

    .flashcard {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #312e81 100%);
        color: white;
        padding: 42px 28px;
        border-radius: 22px;
        text-align: center;
        border: 2px solid #818cf8;
        margin: 16px 0;
        animation: pulseGlow 3.5s infinite, popIn 0.35s ease-out;
        transition: transform 0.25s ease;
    }
    .flashcard:hover {
        transform: translateY(-4px) scale(1.01);
    }

    .gacha-card {
        padding: 22px;
        border-radius: 18px;
        color: white;
        animation: popIn 0.4s ease-out;
        margin-bottom: 12px;
    }
    .rarity-SSR { background: linear-gradient(135deg, #f59e0b 0%, #ea580c 50%, #db2777 100%); border: 2px solid #fde047; box-shadow: 0 0 22px rgba(245, 158, 11, 0.6); }
    .rarity-SR  { background: linear-gradient(135deg, #7c3aed 0%, #4f46e5 100%); border: 2px solid #c4b5fd; box-shadow: 0 0 18px rgba(124, 58, 237, 0.5); }
    .rarity-R   { background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%); border: 2px solid #7dd3fc; }

    .badge-box {
        display: inline-block;
        padding: 8px 14px;
        border-radius: 12px;
        margin: 4px;
        font-size: 0.85rem;
        font-weight: 700;
    }
    .badge-unlocked { background: #ecfdf5; color: #047857; border: 1.5px solid #10b981; }
    .badge-locked   { background: #f1f5f9; color: #94a3b8; border: 1.5px dashed #cbd5e1; }

    .quiz-box {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
        color: white;
        padding: 28px;
        border-radius: 18px;
        border: 2px solid #6366f1;
        margin-bottom: 18px;
        animation: popIn 0.3s ease-out;
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
        pass

if "df" not in st.session_state:
    st.session_state.df = load_data()
if "bonus_xp" not in st.session_state:
    st.session_state.bonus_xp = 0
if "best_streak" not in st.session_state:
    st.session_state.best_streak = 0

df = st.session_state.df

# คำนวณ XP และ Rank
mastered = len(df[df["Status"] == "ใช้คล่องแล้ว"])
learning = len(df[df["Status"] == "กำลังเรียน"])
total_skills = len(df)
xp = (mastered * 15) + (learning * 5) + st.session_state.bonus_xp
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
    <div class="hero-title">🎮 Personal Data Analyst Skill Hub</div>
    <div class="hero-sub">อัปสกิล 4 เครื่องมือสาย Data แบบเกม RPG: Excel • SQL • Power BI DAX • Python (Pandas)</div>
    <div class="rank-badge">{get_rank(xp)} &nbsp;|&nbsp; ⭐ {xp:,} XP &nbsp;|&nbsp; 🔥 Best Combo: {st.session_state.best_streak}</div>
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
c1.metric("📚 ฟังก์ชันทั้งหมด", f"{total_skills} ตัว")
c2.metric("✅ ใช้คล่องแล้ว", f"{mastered} ตัว")
c3.metric("⏳ กำลังเรียน", f"{learning} ตัว")
c4.metric("🎯 ความคืบหน้า", f"{progress_pct}%")
st.progress(progress_pct / 100)

# 5 แท็บหลัก
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎰 กาชาสกิล & เหรียญตรา",
    "🃏 Flashcards เรืองแสง",
    "⚔️ เกมทายฟังก์ชัน (4 ตัวเลือก)",
    "🔀 เทียบสูตร 4 เครื่องมือ",
    "📚 คลัง 120 ฟังก์ชัน"
])

# ==========================================
# TAB 1: SKILL GACHA & ACHIEVEMENTS
# ==========================================
with tab1:
    col_l, col_r = st.columns([1.2, 1])

    with col_l:
        st.subheader("🎰 ตู้กาชาสุ่มสกิลประจำวัน")
        st.caption("กดสุ่มเพื่อรับภารกิจฝึกฟังก์ชัน พร้อมลุ้นระดับความหายาก R / SR / SSR!")

        unmastered = df[df["Status"] != "ใช้คล่องแล้ว"]
        if len(unmastered) == 0:
            st.success("🎉 สุดยอด! คุณปลดล็อกครบทั้ง 120 ฟังก์ชันแล้ว!")
        else:
            if "gacha_idx" not in st.session_state or st.session_state.gacha_idx not in unmastered.index:
                st.session_state.gacha_idx = random.choice(unmastered.index.tolist())
                st.session_state.gacha_rarity = random.choices(["R", "SR", "SSR"], weights=[55, 30, 15])[0]

            g_row = df.loc[st.session_state.gacha_idx]
            rarity = st.session_state.gacha_rarity
            rarity_label = {"SSR": "🌟 SSR (Legendary Skill)", "SR": "💎 SR (Epic Skill)", "R": "🔹 R (Core Skill)"}[rarity]

            st.markdown(f"""
            <div class="gacha-card rarity-{rarity}">
                <div style="font-size:0.85rem; font-weight:800; letter-spacing:1px; opacity:0.95;">{rarity_label} • {g_row['Category']}</div>
                <div style="font-size:1.9rem; font-weight:900; margin:8px 0;">{g_row['Function']}</div>
                <div style="font-size:1rem; margin-bottom:12px;">{g_row['Description']}</div>
                <div style="background:rgba(0,0,0,0.35); padding:10px 14px; border-radius:10px; font-family:monospace; font-size:0.88rem; color:#fef08a;">
                    {g_row['Example']}
                </div>
            </div>
            """, unsafe_allow_html=True)

            gb1, gb2, gb3 = st.columns(3)
            if gb1.button("🎲 กดสุ่มกาชาใหม่!", use_container_width=True):
                st.session_state.gacha_idx = random.choice(unmastered.index.tolist())
                st.session_state.gacha_rarity = random.choices(["R", "SR", "SSR"], weights=[55, 30, 15])[0]
                if st.session_state.gacha_rarity == "SSR":
                    st.toast("🌟 โอ้โห! สุ่มได้การ์ดระดับ SSR!", icon="🎉")
                    st.snow()
                st.rerun()
            if gb2.button("⏳ รับเข้าคลังเรียน (+5 XP)", use_container_width=True):
                st.session_state.df.at[st.session_state.gacha_idx, "Status"] = "กำลังเรียน"
                save_data(st.session_state.df)
                st.toast("บันทึกเป็น 'กำลังเรียน' แล้ว! +5 XP", icon="⏳")
                st.rerun()
            if gb3.button("✅ เคลียร์ภารกิจ! (+15 XP)", type="primary", use_container_width=True):
                st.session_state.df.at[st.session_state.gacha_idx, "Status"] = "ใช้คล่องแล้ว"
                save_data(st.session_state.df)
                st.toast("เคลียร์ภารกิจสำเร็จ! +15 XP", icon="🏆")
                st.balloons()
                st.session_state.gacha_idx = random.choice(df.index.tolist())
                st.rerun()

    with col_r:
        st.subheader("🏅 เหรียญตราความสำเร็จ (Achievements)")
        excel_done = len(df[(df["Category"] == "Excel") & (df["Status"] == "ใช้คล่องแล้ว")])
        sql_done = len(df[(df["Category"] == "SQL") & (df["Status"] == "ใช้คล่องแล้ว")])

        badges = [
            ("🌱 ก้าวแรกสาย Data (คล่อง ≥ 1 ตัว)", mastered >= 1),
            ("🔥 นักล่าสกิล (คล่อง ≥ 10 ตัว)", mastered >= 10),
            ("⚡ Combo Master (ทายถูก 3 ข้อติด)", st.session_state.best_streak >= 3),
            ("📗 Excel Starter (Excel ≥ 5 ตัว)", excel_done >= 5),
            ("🗄️ SQL Hunter (SQL ≥ 5 ตัว)", sql_done >= 5),
            ("👑 Data Legend (XP ≥ 500)", xp >= 500),
        ]
        badge_html = ""
        for name, unlocked in badges:
            cls = "badge-unlocked" if unlocked else "badge-locked"
            icon = "🔓 " if unlocked else "🔒 "
            badge_html += f'<span class="badge-box {cls}">{icon}{name}</span>'
        st.markdown(badge_html, unsafe_allow_html=True)

        st.divider()
        st.subheader("📈 ความคืบหน้าแต่ละเครื่องมือ")
        for cat in df["Category"].unique():
            sub = df[df["Category"] == cat]
            done = len(sub[sub["Status"] == "ใช้คล่องแล้ว"])
            pct = int((done / len(sub)) * 100) if len(sub) > 0 else 0
            st.write(f"**{cat}** ({done}/{len(sub)}) — {pct}%")
            st.progress(pct / 100)

# ==========================================
# TAB 2: GLOWING FLASHCARDS
# ==========================================
with tab2:
    st.subheader("🃏 การ์ดทบทวนความจำ (Flashcards)")
    fc_cat = st.selectbox("เลือกหมวดที่อยากทบทวน:", ["ทั้งหมด"] + list(df["Category"].unique()), key="fc_cat_sel")
    fc_pool = df if fc_cat == "ทั้งหมด" else df[df["Category"] == fc_cat]

    if "fc_idx" not in st.session_state or st.session_state.fc_idx not in fc_pool.index:
        st.session_state.fc_idx = random.choice(fc_pool.index.tolist())
        st.session_state.fc_flip = False

    card = df.loc[st.session_state.fc_idx]

    answer_html = (
        f"<hr style='border-color:#4f46e5; margin:20px 0;'>"
        f"<div style='font-size:1.15rem; color:#f1f5f9; font-weight:500;'>{card['Description']}</div>"
        f"<div style='margin-top:16px; background:#020617; padding:14px; border-radius:12px; font-family:monospace; color:#34d399; font-size:0.95rem;'>{card['Example']}</div>"
        if st.session_state.fc_flip
        else "<div style='margin-top:18px; color:#94a3b8; font-size:0.95rem;'>นึกในใจก่อนว่าฟังก์ชันนี้ใช้ทำอะไร แล้วกดปุ่มพลิกการ์ดด้านล่าง 👇</div>"
    )

    st.markdown(f"""
    <div class="flashcard">
        <div style="font-size:0.9rem; color:#c4b5fd; font-weight:600; margin-bottom:8px;">{card['Category']} • สถานะปัจจุบัน: {card['Status']}</div>
        <div style="font-size:2.4rem; font-weight:900; color:#ffffff;">{card['Function']}</div>
        {answer_html}
    </div>
    """, unsafe_allow_html=True)

    f1, f2, f3, f4 = st.columns(4)
    if f1.button("🔄 พลิกดูเฉลย", use_container_width=True):
        st.session_state.fc_flip = not st.session_state.fc_flip
        st.rerun()
    if f2.button("😅 ยังงงอยู่ (สุ่มใหม่)", use_container_width=True):
        st.session_state.fc_idx = random.choice(fc_pool.index.tolist())
        st.session_state.fc_flip = False
        st.rerun()
    if f3.button("🤔 พอคุ้นๆ (+5 XP)", use_container_width=True):
        st.session_state.df.at[st.session_state.fc_idx, "Status"] = "กำลังเรียน"
        save_data(st.session_state.df)
        st.toast("อัปเดตเป็น 'กำลังเรียน' แล้ว! +5 XP", icon="⏳")
        st.session_state.fc_idx = random.choice(fc_pool.index.tolist())
        st.session_state.fc_flip = False
        st.rerun()
    if f4.button("🔥 จำแม่นแล้ว (+15 XP)", type="primary", use_container_width=True):
        st.session_state.df.at[st.session_state.fc_idx, "Status"] = "ใช้คล่องแล้ว"
        save_data(st.session_state.df)
        st.toast("ยอดเยี่ยม! ปลดล็อกเป็น 'ใช้คล่องแล้ว' +15 XP", icon="🔥")
        st.session_state.fc_idx = random.choice(fc_pool.index.tolist())
        st.session_state.fc_flip = False
        st.rerun()

# ==========================================
# TAB 3: KAHOOT-STYLE MINI GAME (HP + COMBO + 4 BUTTONS)
# ==========================================
with tab3:
    st.subheader("⚔️ เกมทายฟังก์ชันสาย Data (กดตัวเลือกได้เลย!)")

    if "quiz_hp" not in st.session_state:
        st.session_state.quiz_hp = 3
        st.session_state.quiz_score = 0
        st.session_state.quiz_streak = 0
        st.session_state.quiz_cat = "ทั้งหมด"

    def new_question(cat_filter="ทั้งหมด"):
        pool = df if cat_filter == "ทั้งหมด" else df[df["Category"] == cat_filter]
        target = pool.sample(1).iloc[0]
        same_cat = df[(df["Category"] == target["Category"]) & (df["Function"] != target["Function"])]
        wrong_choices = same_cat.sample(min(3, len(same_cat)))["Function"].tolist()
        options = wrong_choices + [target["Function"]]
        random.shuffle(options)
        st.session_state.q_target = target.to_dict()
        st.session_state.q_options = options
        st.session_state.q_answered = False
        st.session_state.q_picked = None

    if "q_target" not in st.session_state:
        new_question()

    # แถบควบคุมหมวด + สถานะเกม
    gc1, gc2, gc3, gc4 = st.columns([1.4, 1, 1, 1])
    chosen_cat = gc1.selectbox("โหมดหมวดหมู่:", ["ทั้งหมด"] + list(df["Category"].unique()), key="quiz_cat_sel")
    if chosen_cat != st.session_state.quiz_cat:
        st.session_state.quiz_cat = chosen_cat
        new_question(chosen_cat)
        st.rerun()

    hearts = "❤️" * st.session_state.quiz_hp + "🖤" * (3 - st.session_state.quiz_hp)
    gc2.metric("พลังชีวิต (HP)", hearts)
    gc3.metric("🏆 คะแนน", f"{st.session_state.quiz_score} แต้ม")
    gc4.metric("🔥 คอมโบ", f"{st.session_state.quiz_streak} ข้อติด")

    # เช็ก Game Over
    if st.session_state.quiz_hp <= 0:
        st.error(f"💀 GAME OVER! หัวใจหมดแล้ว — รอบนี้คุณทำได้ **{st.session_state.quiz_score} แต้ม** (คอมโบสูงสุด {st.session_state.best_streak})")
        if st.button("🔄 เริ่มเล่นรอบใหม่ (รีเซ็ตหัวใจ ❤️❤️❤️)", type="primary", use_container_width=True):
            st.session_state.quiz_hp = 3
            st.session_state.quiz_score = 0
            st.session_state.quiz_streak = 0
            new_question(st.session_state.quiz_cat)
            st.rerun()
    else:
        q = st.session_state.q_target
        st.markdown(f"""
        <div class="quiz-box">
            <div style="font-size:0.9rem; color:#a5b4fc; font-weight:700;">หมวด: {q['Category']} — ฟังก์ชันใดทำหน้าที่นี้?</div>
            <div style="font-size:1.5rem; font-weight:800; margin-top:10px;">"{q['Description']}"</div>
        </div>
        """, unsafe_allow_html=True)

        # ปุ่มตัวเลือก 4 ปุ่มแบบ 2x2 Grid
        opts = st.session_state.q_options
        labels = ["🅰️ ", "🅱️ ", "🇨 ", "🇩 "]
        row1_c1, row1_c2 = st.columns(2)
        row2_c1, row2_c2 = st.columns(2)
        grid_cols = [row1_c1, row1_c2, row2_c1, row2_c2]

        for i, opt in enumerate(opts):
            if grid_cols[i].button(
                f"{labels[i]} {opt}",
                key=f"opt_btn_{i}",
                disabled=st.session_state.q_answered,
                use_container_width=True
            ):
                st.session_state.q_answered = True
                st.session_state.q_picked = opt
                if opt == q["Function"]:
                    st.session_state.quiz_score += 10
                    st.session_state.quiz_streak += 1
                    st.session_state.bonus_xp += 5
                    if st.session_state.quiz_streak > st.session_state.best_streak:
                        st.session_state.best_streak = st.session_state.quiz_streak
                    st.toast(f"🎉 ถูกต้อง! +10 แต้ม (+5 XP) | 🔥 Combo x{st.session_state.quiz_streak}", icon="✅")
                    if st.session_state.quiz_streak % 3 == 0:
                        st.balloons()
                else:
                    st.session_state.quiz_hp -= 1
                    st.session_state.quiz_streak = 0
                    st.toast("❌ พลาดไปนิดเดียว! เสียหัวใจ 1 ดวง 💔", icon="💔")
                st.rerun()

        if st.session_state.q_answered:
            if st.session_state.q_picked == q["Function"]:
                st.success(f"🎉 ถูกต้องครับ! คำตอบคือ **{q['Function']}**\n\nตัวอย่างโค้ด: `{q['Example']}`")
            else:
                st.error(f"❌ คุณตอบ `{st.session_state.q_picked}` — คำตอบที่ถูกคือ **{q['Function']}**\n\nตัวอย่างโค้ด: `{q['Example']}`")

            if st.button("➡️ ลุยข้อถัดไป!", type="primary", use_container_width=True):
                new_question(st.session_state.quiz_cat)
                st.rerun()

# ==========================================
# TAB 4: CROSS-TOOL TRANSLATOR
# ==========================================
with tab4:
    st.subheader("🔀 เทียบสูตรข้าม 4 เครื่องมือ (ทำงานเดียวกัน เขียนต่างกันยังไง?)")
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
        st.toast("บันทึกสถานะและอัปเดต XP เรียบร้อยแล้ว!", icon="💾")
        st.rerun()
