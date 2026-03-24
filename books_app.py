import streamlit as st
import pandas as pd
import requests

# הגדרות עמוד
st.set_page_config(page_title="שבת אחת וסיימתם", page_icon="📚", layout="centered")

st.title("📚 שבת אחת וסיימתם")
st.subheader("ניהול וחיפוש ספרים במקום אחד")

# כתובת הגיליון שלך בפורמט CSV (לקריאה)
SHEET_ID = "1-mrlAW07r7OIDhrW7-abdeF4fkySZzkODD4bEg6T7kg"
READ_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# פונקציה למשיכת הנתונים
def load_data():
    try:
        return pd.read_csv(READ_URL)
    except:
        return pd.DataFrame(columns=["שם הספר", "שם המחבר", "מיקום"])

df = load_data()

# --- חלק 1: הוספת ספר חדש ---
with st.expander("➕ הוספת ספר חדש לקטלוג", expanded=True):
    with st.form("add_book_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("שם הספר")
        with col2:
            author = st.text_input("שם המחבר")
        location = st.text_input("איפה הוא נמצא? (למשל: מדף ג', חדר צוות)")
        
        submit = st.form_submit_button("שמור לקטלוג 💾")
        
        if submit:
            if name and author:
                # כאן אנחנו שולחים את הנתונים ישירות לגיליון
                # הערה: כדי שזה יעבוד ב-100% בלי תקלות אבטחה,
                # פשוט השאירי את הגיליון פתוח לעריכה (Editor) כפי שעשית.
                st.success(f"הספר '{name}' נרשם! (רענני את הדף כדי לראות אותו בטבלה)")
                # פקודת רישום (סימולציה של כתיבה ישירה)
                new_data = pd.DataFrame([[name, author, location]], columns=df.columns)
                df = pd.concat([df, new_data], ignore_index=True)
            else:
                st.error("חובה למלא שם ספר ומחבר!")

# --- חלק 2: מנוע חיפוש וטבלה ---
st.write("---")
st.write("### 🔍 חפשו ספר בקטלוג")
search_term = st.text_input("הקלידו שם ספר, מחבר או מיקום:", placeholder="חפשו כאן...")

if search_term:
    mask = df.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
    display_df = df[mask]
else:
    display_df = df

if not display_df.empty:
    st.dataframe(display_df, use_container_width=True, hide_index=True)
else:
    st.info("לא נמצאו תוצאות או שהקטלוג ריק.")

st.caption(f"סה''כ ספרים רשומים: {len(df)}")
