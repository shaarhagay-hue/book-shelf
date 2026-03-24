import streamlit as st
import pandas as pd
import time

# הגדרות עמוד - כותרת ועיצוב
st.set_page_config(page_title="שבת אחת וסיימתם", page_icon="📚", layout="centered")

st.title("📚 שבת אחת וסיימתם")
st.subheader("ניהול וחיפוש ספרים במקום אחד")

# --- חלק 1: הוספת ספר (דרך טופס גוגל מוטמע) ---
with st.expander("➕ הוספת ספר חדש לקטלוג", expanded=True):
    # הקישור ששלחת מוטמע כאן:
    google_form_url = "https://docs.google.com/forms/d/e/1FAIpQLSet8S6RvBmV-OLtFlRrBe3SBfpnwIkjekwOrYvlMyE2XER0Xw/viewform" 
    
    st.markdown(f'<iframe src="{google_form_url}" width="100%" height="600" frameborder="0" marginheight="0" marginwidth="0">טוען...</iframe>', unsafe_allow_html=True)
    st.info("💡 לאחר לחיצה על 'שליחה' בטופס, רעננו את הדף (F5) כדי לראות את הספר בטבלה למטה.")

# --- חלק 2: מנוע חיפוש ותצוגת הספרים ---
st.write("---")
st.write("### 🔍 חפשו ספר בקטלוג")

# משיכת הנתונים מגיליון הגוגל (CSV Export עם מנגנון רענון)
SHEET_ID = "1-mrlAW07r7OIDhrW7-abdeF4fkySZzkODD4bEg6T7kg"
t = int(time.time()) # מונע מהדפדפן להציג נתונים ישנים מהזיכרון
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&cachebust={t}"

try:
    # קריאת הנתונים וניקוי שורות ריקות
    df = pd.read_csv(url).dropna(how="all")
    
    # תיבת חיפוש
    search_term = st.text_input("הקלידו שם ספר, מחבר או מיקום:", placeholder="למשל: מאיר שלו...")
    
    if search_term:
        # סינון הטבלה לפי מילת החיפוש
        mask = df.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
        display_df = df[mask]
    else:
        display_df = df

    # הצגת הטבלה
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    st.caption(f"סה''כ ספרים רשומים במערכת: {len(df)}")

except Exception as e:
    st.warning("הקטלוג עדיין ריק או בטעינה. ברגע שתשלחו את הספר הראשון בטופס, הוא יופיע כאן.")
