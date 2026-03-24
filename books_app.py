import streamlit as st
import pandas as pd
import gspread

# הגדרות עמוד
st.set_page_config(page_title="שבת אחת וסיימתם", page_icon="📚", layout="centered")

# כותרת האפליקציה
st.title("📚 שבת אחת וסיימתם")
st.subheader("קטלוג הספרים המשותף של הצוות")

# פונקציה לחיבור לגיליון גוגל
def get_data():
    url = "https://docs.google.com/spreadsheets/d/1-mrlAW07r7OIDhrW7-abdeF4fkySZzkODD4bEg6T7kg/edit?usp=sharing"
    # חיבור ציבורי לקריאה
    try:
        csv_url = url.replace('/edit?usp=sharing', '/export?format=csv')
        df = pd.read_csv(csv_url)
        return df.dropna(how="all")
    except:
        return pd.DataFrame(columns=["שם הספר", "שם המחבר", "מיקום"])

df = get_data()

# --- תפריט צד להוספת ספר חדש ---
st.sidebar.header("➕ הוספת ספר חדש")
with st.sidebar.form("add_form", clear_on_submit=True):
    new_name = st.text_input("שם הספר")
    new_author = st.text_input("שם המחבר")
    new_loc = st.text_input("איפה הוא נמצא? (מדף/חדר)")
    
    submit = st.form_submit_button("הוסף לקטלוג")
    
    if submit:
        if new_name and new_author:
            st.sidebar.warning("שימי לב: כדי לאפשר הוספה, עלייך להגדיר הרשאות 'עורך' בגיליון הגוגל לכל מי שיש לו קישור.")
            # כאן המקום להוסיף לוגיקת כתיבה אם תרצי בהמשך, כרגע נתמקד בהצגת הנתונים
            st.sidebar.info("הנתונים נשמרים בגיליון הגוגל שלך.")
        else:
            st.sidebar.error("חובה למלא שם ספר ומחבר")

# --- חיפוש ותצוגה ---
st.write("---")
search = st.text_input("🔍 חפשו ספר, מחבר או מיקום:", placeholder="למשל: מאיר שלו, מדף א'...")

if search:
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
        st.info("הקטלוג ריק כרגע או שהחיבור לגיליון נכשל.")

st.write("---")
st.caption(f"סה''כ ספרים רשומים: {len(df)}")
