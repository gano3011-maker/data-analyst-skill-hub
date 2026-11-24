import streamlit as st
import pandas as pd
import random
from datetime import date

st.set_page_config(page_title="Data Analyst Skill & Portfolio Hub", page_icon="🚀", layout="wide")

# ==========================================
# CUSTOM CSS ANIMATIONS & CLEAN UI
# ==========================================
st.markdown("""
<style>
@keyframes gradientBG {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
@keyframes pulseGlow {
    0%, 100% { box-shadow: 0 0 15px rgba(99, 102, 241, 0.35); }
    50% { box-shadow: 0 0 26px rgba(236, 72, 153, 0.65); }
}
.hero-box {
    background: linear-gradient(-45deg, #4f46e5, #7c3aed, #ec4899, #06b6d4);
    background-size: 300% 300%;
    animation: gradientBG 8s ease infinite;
    padding: 24px 28px;
    border-radius: 18px;
    color: white;
    margin-bottom: 18px;
    box-shadow: 0 8px 20px rgba(79, 70, 229, 0.2);
}
.hero-title { font-size: 1.9rem; font-weight: 800; margin: 0; }
.hero-sub { font-size: 0.92rem; opacity: 0.92; margin-top: 4px; }
.rank-badge {
    display: inline-block;
    background: rgba(255, 255, 255, 0.22);
    padding: 6px 14px;
    border-radius: 999px;
    font-weight: 700;
    font-size: 0.88rem;
    margin-top: 12px;
    border: 1px solid rgba(255,255,255,0.35);
}
.flashcard {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #312e81 100%);
    color: white;
    padding: 38px 24px;
    border-radius: 20px;
    text-align: center;
    border: 2px solid #818cf8;
    margin: 14px 0;
    animation: pulseGlow 3.5s infinite;
}
.gacha-card {
    padding: 20px;
    border-radius: 16px;
    color: white;
    margin-bottom: 12px;
}
.rarity-SSR { background: linear-gradient(135deg, #f59e0b 0%, #ea580c 50%, #db2777 100%); border: 2px solid #fde047; }
.rarity-SR  { background: linear-gradient(135deg, #7c3aed 0%, #4f46e5 100%); border: 2px solid #c4b5fd; }
.rarity-R   { background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%); border: 2px solid #7dd3fc; }
.badge-box {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 10px;
    margin: 4px;
    font-size: 0.8rem;
    font-weight: 700;
}
.badge-unlocked { background: #ecfdf5; color: #047857; border: 1.5px solid #10b981; }
.badge-locked   { background: #f1f5f9; color: #94a3b8; border: 1.5px dashed #cbd5e1; }
.quiz-box {
    background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
    color: white;
    padding: 24px;
    border-radius: 16px;
    border: 2px solid #6366f1;
    margin-bottom: 16px;
}
.proj-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-top: 5px solid #4f46e5;
    border-radius: 14px;
    padding: 18px 20px;
    margin-bottom: 16px;
    box-shadow: 0 4px 10px rgba(15, 23, 42, 0.05);
    color: #1e293b;
}
.proj-impact {
    background: #f0fdf4;
    border-left: 3px solid #10b981;
    padding: 8px 12px;
    border-radius: 6px;
    font-size: 0.85rem;
    color: #065f46;
    margin: 10px 0;
}
.tool-tag {
    display: inline-block;
    background: #ede9fe;
    color: #5b21b6;
    padding: 3px 10px;
    border-radius: 999px;
    font-size: 0.76rem;
    font-weight: 600;
    margin: 3px 5px 0 0;
}
</style>
""", unsafe_allow_html=True)

SKILLS_FILE = "skills.csv"
PROJECTS_FILE = "projects.csv"

def load_skills():
    return pd.read_csv(SKILLS_FILE)

def save_skills(df):
    try:
        df.to_csv(SKILLS_FILE, index=False)
    except Exception:
        pass

def load_projects():
    try:
        return pd.read_csv(PROJECTS_FILE).fillna("")
    except Exception:
        return pd.DataFrame(columns=["Date", "Project_Name", "Category", "Tools", "Impact", "Link", "Description"])

def save_projects(pdf):
    try:
        pdf.to_csv(PROJECTS_FILE, index=False)
    except Exception:
        pass

if "df" not in st.session_state:
    st.session_state.df = load_skills()
if "proj_df" not in st.session_state:
    st.session_state.proj_df = load_projects()
if "bonus_xp" not in st.session_state:
    st.session_state.bonus_xp = 0
if "best_streak" not in st.session_state:
    st.session_state.best_streak = 0

df = st.session_state.df
proj_df = st.session_state.proj_df

mastered = len(df[df["Status"] == "ใช้คล่องแล้ว"])
learning = len(df[df["Status"] == "กำลังเรียน"])
total_skills = len(df)
total_projects = len(proj_df)

xp = (mastered * 15) + (learning * 5) + (total_projects * 50) + st.session_state.bonus_xp
progress_pct = int((mastered / total_skills) * 100) if total_skills > 0 else 0

def get_rank(points):
    if points >= 1500: return "👑 Lv.5 Data Master"
    if points >= 900:  return "🧙‍♂️ Lv.4 Analytics Wizard"
    if points >= 450:  return "⚡ Lv.3 Query Explorer"
    if points >= 150:  return "🛠️ Lv.2 Data Apprentice"
    return "🌱 Lv.1 Data Rookie"

# Header Banner
st.markdown(
    f'<div class="hero-box">'
    f'<div class="hero-title">🚀 Personal Data Analyst Skill & Portfolio Hub</div>'
    f'<div class="hero-sub">คลังเก็บผลงานจริง + แพลตฟอร์มอัปสกิลสาย Data (Excel • SQL • Power BI DAX • Python • Automation)</div>'
    f'<div class="rank-badge">{get_rank(xp)} &nbsp;|&nbsp; ⭐ {xp:,} XP &nbsp;|&nbsp; 🏆 {total_projects} ผลงานจริง &nbsp;|&nbsp; 🔥 Best Combo: {st.session_state.best_streak}</div>'
    f'</div>',
    unsafe_allow_html=True
)

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("🏆 ผลงานจริง", f"{total_projects} โปรเจกต์")
c2.metric("📚 สกิลทั้งหมด", f"{total_skills} ตัว")
c3.metric("✅ ใช้คล่องแล้ว", f"{mastered} ตัว")
c4.metric("⏳ กำลังเรียน", f"{learning} ตัว")
c5.metric("🎯 ความคืบหน้า", f"{progress_pct}%")
st.progress(progress_pct / 100)

tab_port, tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏆 พอร์ตผลงาน & สถิติ",
    "🎰 กาชาสกิล & เหรียญตรา",
    "🃏 Flashcards เรืองแสง",
    "⚔️ เกมทายฟังก์ชัน",
    "🔀 เทียบสูตร 4 เครื่องมือ",
    "📚 คลัง 120 ฟังก์ชัน"
])

# ==========================================
# TAB 0: CLEAN PORTFOLIO & EXPERIENCE HUB
# ==========================================
with tab_port:
    # ส่วนบน: กราฟสถิติ (ซ้าย) + จัดการพอร์ต & ดาวน์โหลด (ขวา)
    top_l, top_r = st.columns([1.4, 1], gap="large")

    with top_l:
        st.subheader("📊 สถิติทักษะจากผลงานจริง")
        if len(proj_df) > 0:
            all_tools = []
            for t_str in proj_df["Tools"]:
                all_tools.extend([t.strip() for t in str(t_str).split(",") if t.strip()])
            if all_tools:
                tool_counts = pd.Series(all_tools).value_counts().reset_index()
                tool_counts.columns = ["เครื่องมือ", "จำนวนโปรเจกต์"]
                st.bar_chart(tool_counts.set_index("เครื่องมือ"), height=240)
        else:
            st.info("ยังไม่มีข้อมูลสถิติ ลองเพิ่มผลงานแรกของคุณได้เลยครับ")

    with top_r:
        st.subheader("⚙️ จัดการพอร์ต & ส่งออก")
        with st.expander("➕ เพิ่มผลงาน / โปรเจกต์ใหม่ (+50 XP)", expanded=False):
            with st.form("add_project_form", clear_on_submit=True):
                p_name = st.text_input("ชื่อโปรเจกต์ / ผลงาน *")
                p_date = st.date_input("วันที่ทำสำเร็จ", value=date.today())
                p_cat = st.selectbox("หมวดหมู่", [
                    "BI & Dashboard", "Data Automation / RPA", "Data App / Portfolio",
                    "Data Analysis / Research", "SQL & Database", "อื่นๆ"
                ])
                p_tools = st.multiselect("เครื่องมือที่ใช้ *", [
                    "Excel", "VBA Macro", "SQL", "Power BI", "Python", "Pandas",
                    "Streamlit", "Google Apps Script", "Google Sheets",
                    "Power Automate Desktop", "AppSheet", "SPSS", "HTML/JS"
                ])
                p_impact = st.text_input("ผลลัพธ์ทางธุรกิจ (Impact) *", placeholder="เช่น ลดเวลาทำงาน 80% / จัดการข้อมูล 1,000+ รายการ")
                p_desc = st.text_area("รายละเอียดสั้นๆ", placeholder="อธิบายว่าทำอะไรและแก้ปัญหาอะไร")
                p_link = st.text_input("ลิงก์ผลงาน / GitHub (ถ้ามี)")

                if st.form_submit_button("💾 บันทึกผลงานเข้าพอร์ต", type="primary", use_container_width=True):
                    if not p_name or not p_tools or not p_impact:
                        st.error("กรุณากรอก ชื่อโปรเจกต์, เครื่องมือที่ใช้ และผลลัพธ์ทางธุรกิจ ให้ครบครับ")
                    else:
                        new_row = pd.DataFrame([{
                            "Date": str(p_date),
                            "Project_Name": p_name,
                            "Category": p_cat,
                            "Tools": ", ".join(p_tools),
                            "Impact": p_impact,
                            "Link": p_link,
                            "Description": p_desc
                        }])
                        st.session_state.proj_df = pd.concat([st.session_state.proj_df, new_row], ignore_index=True)
                        save_projects(st.session_state.proj_df)
                        st.toast("🎉 เพิ่มผลงานใหม่เข้าพอร์ตแล้ว! +50 XP", icon="🏆")
                        st.balloons()
                        st.rerun()

        md_lines = [f"# Data Analyst Portfolio & Skill Summary\n- **Rank:** {get_rank(xp)} ({xp:,} XP)\n- **Verified Projects:** {total_projects}\n- **Core Skills Mastered:** {mastered}/{total_skills}\n\n## Featured Projects\n"]
        for _, r in proj_df.iterrows():
            md_lines.append(f"### {r['Project_Name']} ({r['Date']})\n- **Tools:** {r['Tools']}\n- **Impact:** {r['Impact']}\n- **Detail:** {r['Description']}\n")
        resume_md = "\n".join(md_lines)

        st.download_button("📄 โหลดสรุปพอร์ตสำหรับ Resume (.md)", data=resume_md, file_name="data_portfolio_summary.md", mime="text/markdown", use_container_width=True)
        d1, d2 = st.columns(2)
        d1.download_button("💾 สำรอง projects.csv", data=proj_df.to_csv(index=False).encode("utf-8-sig"), file_name="projects.csv", mime="text/csv", use_container_width=True)
        d2.download_button("💾 สำรอง skills.csv", data=df.to_csv(index=False).encode("utf-8-sig"), file_name="skills.csv", mime="text/csv", use_container_width=True)

    st.divider()

    # ส่วนล่าง: การ์ดผลงานแบบ 2 คอลัมน์เป็นระเบียบ (ไม่มีบั๊กโค้ดทะลุ)
    st.subheader("📂 ผลงานและประสบการณ์จริง (Verified Projects)")
    if len(proj_df) == 0:
        st.info("ยังไม่มีรายการผลงาน กดปุ่ม '➕ เพิ่มผลงาน / โปรเจกต์ใหม่' ด้านบนได้เลยครับ!")
    else:
        sorted_proj = proj_df.sort_values(by="Date", ascending=False).reset_index(drop=True)
        grid_cols = st.columns(2, gap="medium")
        for idx, row in sorted_proj.iterrows():
            tools_list = [t.strip() for t in str(row["Tools"]).split(",") if t.strip()]
            tags_html = "".join([f'<span class="tool-tag">{t}</span>' for t in tools_list])
            link_str = str(row["Link"]).strip()
            link_html = f'<a href="{link_str}" target="_blank" style="color:#4f46e5; font-weight:700; text-decoration:none; font-size:0.85rem;">🔗 เปิดดูผลงาน</a>' if link_str else ""

            card_html = (
                f'<div class="proj-card">'
                f'<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">'
                f'<span style="font-size:0.78rem; color:#64748b; font-weight:600;">📅 {row["Date"]} • {row["Category"]}</span>'
                f'{link_html}'
                f'</div>'
                f'<div style="font-size:1.18rem; font-weight:800; color:#0f172a; margin-bottom:6px;">{row["Project_Name"]}</div>'
                f'<div style="font-size:0.88rem; color:#475569; line-height:1.5;">{row["Description"]}</div>'
                f'<div class="proj-impact"><b>📈 Impact:</b> {row["Impact"]}</div>'
                f'<div>{tags_html}</div>'
                f'</div>'
            )
            with grid_cols[idx % 2]:
                st.markdown(card_html, unsafe_allow_html=True)

# ==========================================
# TAB 1: SKILL GACHA & ACHIEVEMENTS
# ==========================================
with tab1:
    col_l, col_r = st.columns([1.2, 1], gap="large")
    with col_l:
        st.subheader("🎰 ตู้กาชาสุ่มสกิลประจำวัน")
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

            st.markdown(
                f'<div class="gacha-card rarity-{rarity}">'
                f'<div style="font-size:0.85rem; font-weight:800; letter-spacing:1px;">{rarity_label} • {g_row["Category"]}</div>'
                f'<div style="font-size:1.8rem; font-weight:900; margin:8px 0;">{g_row["Function"]}</div>'
                f'<div style="font-size:0.95rem; margin-bottom:12px;">{g_row["Description"]}</div>'
                f'<div style="background:rgba(0,0,0,0.35); padding:10px 14px; border-radius:10px; font-family:monospace; font-size:0.86rem; color:#fef08a;">{g_row["Example"]}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

            gb1, gb2, gb3 = st.columns(3)
            if gb1.button("🎲 สุ่มกาชาใหม่", use_container_width=True):
                st.session_state.gacha_idx = random.choice(unmastered.index.tolist())
                st.session_state.gacha_rarity = random.choices(["R", "SR", "SSR"], weights=[55, 30, 15])[0]
                if st.session_state.gacha_rarity == "SSR":
                    st.toast("🌟 โอ้โห! สุ่มได้การ์ดระดับ SSR!", icon="🎉")
                    st.snow()
                st.rerun()
            if gb2.button("⏳ กำลังเรียน (+5 XP)", use_container_width=True):
                st.session_state.df.at[st.session_state.gacha_idx, "Status"] = "กำลังเรียน"
                save_skills(st.session_state.df)
                st.toast("บันทึกเป็น 'กำลังเรียน' แล้ว! +5 XP", icon="⏳")
                st.rerun()
            if gb3.button("✅ เคลียร์! (+15 XP)", type="primary", use_container_width=True):
                st.session_state.df.at[st.session_state.gacha_idx, "Status"] = "ใช้คล่องแล้ว"
                save_skills(st.session_state.df)
                st.toast("เคลียร์ภารกิจสำเร็จ! +15 XP", icon="🏆")
                st.balloons()
                st.session_state.gacha_idx = random.choice(df.index.tolist())
                st.rerun()

    with col_r:
        st.subheader("🏅 เหรียญตราความสำเร็จ")
        excel_done = len(df[(df["Category"] == "Excel") & (df["Status"] == "ใช้คล่องแล้ว")])
        sql_done = len(df[(df["Category"] == "SQL") & (df["Status"] == "ใช้คล่องแล้ว")])
        badges = [
            ("🏆 Builder ตัวจริง (ผลงาน ≥ 3 ชิ้น)", total_projects >= 3),
            ("🌱 ก้าวแรกสาย Data (คล่อง ≥ 1 ตัว)", mastered >= 1),
            ("🔥 นักล่าสกิล (คล่อง ≥ 10 ตัว)", mastered >= 10),
            ("⚡ Combo Master (ทายถูก 3 ข้อติด)", st.session_state.best_streak >= 3),
            ("📗 Excel Starter (Excel ≥ 5 ตัว)", excel_done >= 5),
            ("🗄️ SQL Hunter (SQL ≥ 5 ตัว)", sql_done >= 5),
            ("👑 Data Legend (XP ≥ 500)", xp >= 500),
        ]
        badge_html = "".join([f'<span class="badge-box {"badge-unlocked" if u else "badge-locked"}">{"🔓 " if u else "🔒 "}{n}</span>' for n, u in badges])
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
        f'<hr style="border-color:#4f46e5; margin:18px 0;">'
        f'<div style="font-size:1.1rem; color:#f1f5f9;">{card["Description"]}</div>'
        f'<div style="margin-top:14px; background:#020617; padding:12px; border-radius:10px; font-family:monospace; color:#34d399; font-size:0.92rem;">{card["Example"]}</div>'
        if st.session_state.fc_flip
        else '<div style="margin-top:16px; color:#94a3b8; font-size:0.92rem;">นึกในใจก่อนว่าฟังก์ชันนี้ใช้ทำอะไร แล้วกดปุ่มพลิกการ์ดด้านล่าง 👇</div>'
    )

    st.markdown(
        f'<div class="flashcard">'
        f'<div style="font-size:0.88rem; color:#c4b5fd; font-weight:600; margin-bottom:8px;">{card["Category"]} • สถานะ: {card["Status"]}</div>'
        f'<div style="font-size:2.2rem; font-weight:900; color:#ffffff;">{card["Function"]}</div>'
        f'{answer_html}'
        f'</div>',
        unsafe_allow_html=True
    )

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
        save_skills(st.session_state.df)
        st.toast("อัปเดตเป็น 'กำลังเรียน' แล้ว! +5 XP", icon="⏳")
        st.session_state.fc_idx = random.choice(fc_pool.index.tolist())
        st.session_state.fc_flip = False
        st.rerun()
    if f4.button("🔥 จำแม่นแล้ว (+15 XP)", type="primary", use_container_width=True):
        st.session_state.df.at[st.session_state.fc_idx, "Status"] = "ใช้คล่องแล้ว"
        save_skills(st.session_state.df)
        st.toast("ยอดเยี่ยม! ปลดล็อกเป็น 'ใช้คล่องแล้ว' +15 XP", icon="🔥")
        st.session_state.fc_idx = random.choice(fc_pool.index.tolist())
        st.session_state.fc_flip = False
        st.rerun()

# ==========================================
# TAB 3: KAHOOT-STYLE MINI GAME
# ==========================================
with tab3:
    st.subheader("⚔️ เกมทายฟังก์ชันสาย Data")
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
        st.markdown(
            f'<div class="quiz-box">'
            f'<div style="font-size:0.88rem; color:#a5b4fc; font-weight:700;">หมวด: {q["Category"]} — ฟังก์ชันใดทำหน้าที่นี้?</div>'
            f'<div style="font-size:1.4rem; font-weight:800; margin-top:8px;">"{q["Description"]}"</div>'
            f'</div>',
            unsafe_allow_html=True
        )

        opts = st.session_state.q_options
        labels = ["🅰️ ", "🅱️ ", "🇨 ", "🇩 "]
        r1c1, r1c2 = st.columns(2)
        r2c1, r2c2 = st.columns(2)
        grid_cols = [r1c1, r1c2, r2c1, r2c2]

        for i, opt in enumerate(opts):
            if grid_cols[i].button(f"{labels[i]} {opt}", key=f"opt_btn_{i}", disabled=st.session_state.q_answered, use_container_width=True):
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
    st.subheader("🔀 เทียบสูตรข้าม 4 เครื่องมือ")
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
            "Status": st.column_config.SelectboxColumn("สถานะ", options=["ยังไม่เริ่ม", "กำลังเรียน", "ใช้คล่องแล้ว"], required=True),
            "Example": st.column_config.TextColumn("ตัวอย่างการใช้งาน", width="large"),
        },
        disabled=["Category", "Function", "Description"],
        hide_index=True,
        use_container_width=True,
        height=450,
    )

    if st.button("💾 บันทึกความคืบหน้า", type="primary"):
        st.session_state.df.update(edited_df)
        save_skills(st.session_state.df)
        st.toast("บันทึกสถานะและอัปเดต XP เรียบร้อยแล้ว!", icon="💾")
        st.rerun()
