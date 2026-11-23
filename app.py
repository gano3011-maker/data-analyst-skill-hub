import streamlit as st
import pandas as pd

st.set_page_config(page_title="Data Analyst Skill Hub", page_icon="📊", layout="wide")

FILE_PATH = "skills.csv"

# โหลดข้อมูลจากไฟล์ CSV
def load_data():
    return pd.read_csv(FILE_PATH)

def save_data(df):
    df.to_csv(FILE_PATH, index=False)

df = load_data()

st.title("📊 Personal Data Analyst Skill Hub")
st.caption("อัปสกิล 4 เครื่องมือหลักสาย Data (Excel • SQL • Power BI DAX • Python Pandas)")

# แถบแสดงความคืบหน้าภาพรวม (Metrics)
total_skills = len(df)
mastered = len(df[df["Status"] == "ใช้คล่องแล้ว"])
learning = len(df[df["Status"] == "กำลังเรียน"])
progress_pct = int((mastered / total_skills) * 100) if total_skills > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("ฟังก์ชันทั้งหมด", f"{total_skills} ตัว")
col2.metric("ใช้คล่องแล้ว ✅", f"{mastered} ตัว")
col3.metric("กำลังเรียน ⏳", f"{learning} ตัว")
col4.metric("ความคืบหน้า", f"{progress_pct}%")
st.progress(progress_pct / 100)

st.divider()

# ตัวกรองด้านข้าง (Sidebar)
st.sidebar.header("🔍 ตัวกรอง & ค้นหา")
selected_cat = st.sidebar.multiselect(
    "เลือกเครื่องมือ:",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)
selected_status = st.sidebar.multiselect(
    "สถานะการเรียน:",
    options=["ยังไม่เริ่ม", "กำลังเรียน", "ใช้คล่องแล้ว"],
    default=["ยังไม่เริ่ม", "กำลังเรียน", "ใช้คล่องแล้ว"]
)
search_query = st.sidebar.text_input("ค้นหาชื่อฟังก์ชัน / คำอธิบาย:")

# กรองข้อมูลตามที่เลือก
filtered_df = df[
    (df["Category"].isin(selected_cat)) &
    (df["Status"].isin(selected_status))
]
if search_query:
    filtered_df = filtered_df[
        filtered_df["Function"].str.contains(search_query, case=False, na=False) |
        filtered_df["Description"].str.contains(search_query, case=False, na=False)
    ]

# แสดงตารางแบบแก้ไขสถานะได้ทันที
st.subheader(f"รายการฟังก์ชัน ({len(filtered_df)} รายการ)")
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
)

# ปุ่มบันทึกเมื่อเปลี่ยนสถานะ
if st.button("💾 บันทึกความคืบหน้า", type="primary"):
    df.update(edited_df)
    save_data(df)
    st.success("บันทึกสถานะเรียบร้อยแล้ว!")
    st.rerun()