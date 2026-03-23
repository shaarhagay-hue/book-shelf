import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# הגדרות עמוד
st.set_page_config(page_title="שבת אחת וסיימתם", page_icon="📚", layout="centered")

# כותרת האפליקציה
st.title("📚 שבת אחת וסיימתם")
st.subheader("קטלוג הספרים המשותף של הצוות")

# קישור לגיליון הגוגל החדש שלך - נא להחליף בקישור האמיתי!
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1-mrlAW07r7OIDhrW7-abdeF4fkySZzkODD4bEg6T7kg/edit?usp=sharing"

# חיבור לנתונים
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    df = conn.read(spreadsheet=spreadsheet_url)
    if df is None or df.empty:
        df = pd.DataFrame(columns=["שם הספר", "שם המחבר", "מיקום"])
except:
    df = pd.DataFrame(columns=["שם הספר", "שם המחבר", "מיקום"])

df = df.dropna(how="all")

# --- תפריט צד להוספת ספרים ---
st.sidebar.header("➕ הוספת ספר חדש")
with st.sidebar.form("add_form", clear_on_submit=True):
    new_name = st.text_input("שם הספר")
    new_author = st.text_input("שם המחבר")
    new_loc = st.text_input("איפה הוא נמצא? (מדף/חדר)")
    
    submit = st.form_submit_button("הוסף לקטלוג")
    
    if submit:
        if new_name and new_author:
            new_row = pd.DataFrame([{"שם הספר": new_name, "שם המחבר": new_author, "מיקום": new_loc}])
            df = pd.concat([df, new_row], ignore_index=True)
            conn.update(spreadsheet=spreadsheet_url, data=df)
            st.sidebar.success(f"הספר '{new_name}' נוסף בהצלחה!")
            st.rerun()
        else:
            st.sidebar.error("חובה למלא שם ספר ומחבר")

# --- חיפוש ותצוגה ---
st.write("---")
search = st.text_input("🔍 חפשו ספר, מחבר או מיקום:", placeholder="למשל: מאיר שלו, מדף א'...")

if search:
    # חיפוש חכם בכל העמודות
    mask = df.astype(str).apply(lambda x: x.str.contains(search, case=False, na=False)).any(axis=1)
    results = df[mask]
    
    if not results.empty:
        st.dataframe(results, use_container_width=True, hide_index=True)
    else:
        st.warning("לא מצאנו ספר כזה במאגר...")
else:
    if not df.empty:
        st.write("📖 **כל הספרים בקטלוג:**")
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("הקטלוג ריק כרגע. זה הזמן להוסיף את הספר הראשון!")

# סיומת
st.write("---")
st.caption(f"סה''כ ספרים ב-'שבת אחת וסיימתם': {len(df)}")
