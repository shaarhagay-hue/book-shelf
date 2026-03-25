import streamlit as st
import pandas as pd
import time

# הגדרות עמוד
st.set_page_config(page_title="שבת אחת וסיימתם", page_icon="📚", layout="centered")

st.title("📚 שבת אחת וסיימתם")
st.subheader("קטלוג הספרים המשותף")

# --- חלק 1: מנוע חיפוש (מופיע ראשון) ---
st.write("### 🔍 חפשו ספר בקטלוג")
SHEET_ID = "1-mrlAW07r7OIDhrW7-abdeF4fkySZzkODD4bEg6T7kg"
t = int(time.time()) 
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&cachebust={t}"

try:
    df = pd.read_csv(url).dropna(how="all")
    search_term = st.text_input("הקלידו שם ספר, מחבר או מיקום:", placeholder="למשל: מאיר שלו...")
    
    if search_term:
        mask = df.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
        display_df = df[mask]
    else:
        display_df = df
        
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    st.caption(f"סה''כ ספרים רשומים במערכת: {len(df)}")
except Exception as e:
    st.warning("הקטלוג בטעינה או שעדיין לא נוספו ספרים.")

st.write("---")

# --- חלק 2: הוספת ספר (תיבה מתקפלת) ---
with st.expander("➕ הוספת ספר חדש לקטלוג", expanded=False):
    google_form_url = "https://docs.google.com/forms/d/e/1FAIpQLSet8S6RvBmV-OLtFlRrBe3SBfpnwIkjekwOrYvlMyE2XER0Xw/viewform" 
    st.markdown(f'<iframe src="{google_form_url}" width="100%" height="600" frameborder="0" marginheight="0" marginwidth="0">טוען...</iframe>', unsafe_allow_html=True)
    st.info("💡 לאחר לחיצה על 'שליחה' בטופס, רעננו את הדף (F5) כדי לראות את העדכון בטבלה למעלה.")

# --- חלק 3: קישורי ניהול (מוסתרים מעט בתחתית) ---
st.write("")
st.write("")
with st.sidebar:
    st.write("### 🛠 ניהול המערכת")
    sheet_link = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit"
    st.link_button("📝 עריכת נתונים (Google Sheets)", sheet_link)
    st.caption("הכפתור מיועד למנהלת הקטלוג בלבד לצורך תיקון טעויות ומחיקת ספרים.")
