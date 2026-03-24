import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# הגדרות עמוד
st.set_page_config(page_title="שבת אחת וסיימתם", page_icon="📚", layout="centered")

st.title("📚 שבת אחת וסיימתם")
st.subheader("קטלוג הספרים המשותף של הצוות")

# חיבור ישיר לגיליון (נא לוודא שהקישור נכון)
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1-mrlAW07r7OIDhrW7-abdeF4fkySZzkODD4bEg6T7kg/edit?usp=sharing"

# יצירת חיבור
conn = st.connection("gsheets", type=GSheetsConnection)

# פונקציה לטעינת נתונים ללא דיליי (TTL=0)
def load_data():
    return conn.read(spreadsheet=spreadsheet_url, ttl=0)

try:
    df = load_data()
    df = df.dropna(how="all")
except:
    df = pd.DataFrame(columns=["שם הספר", "שם המחבר", "מיקום"])

# --- טופס הוספה ---
with st.expander("➕ הוספת ספר חדש", expanded=True):
    with st.form("add_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            new_name = st.text_input("שם הספר")
        with col2:
            new_author = st.text_input("שם המחבר")
        new_loc = st.text_input("איפה הוא נמצא?")
        
        submit = st.form_submit_button("שמור לקטלוג 💾")
        
        if submit:
            if new_name and new_author:
                # הוספת השורה לטבלה הקיימת
                new_row = pd.DataFrame([{"שם הספר": new_name, "שם המחבר": new_author, "מיקום": new_loc}])
                updated_df = pd.concat([df, new_row], ignore_index=True)
                
                # עדכון הגיליון בגוגל
                conn.update(spreadsheet=spreadsheet_url, data=updated_df)
                st.success(f"הספר '{new_name}' נשמר בהצלחה!")
                st.rerun() # רענון מיידי של האפליקציה להצגת הנתון החדש
            else:
                st.error("חובה למלא שם ספר ומחבר")

# --- חיפוש ותצוגה ---
st.write("---")
search = st.text_input("🔍 חפשו ספר, מחבר או מיקום:")

if search:
    mask = df.astype(str).apply(lambda x: x.str.contains(search, case=False, na=False)).any(axis=1)
    display_df = df[mask]
else:
    display_df = df

st.dataframe(display_df, use_container_width=True, hide_index=True)
st.caption(f"סה''כ ספרים: {len(df)}")
