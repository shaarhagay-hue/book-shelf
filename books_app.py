import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# הגדרות עמוד
st.set_page_config(page_title="שבת אחת וסיימתם", page_icon="📚", layout="centered")

# כותרת האפליקציה
st.title("📚 שבת אחת וסיימתם")
st.subheader("קטלוג הספרים המשותף של הצוות")

# חיבור ישיר לנתונים (עוקף את ה-Secrets כדי למנוע שגיאות הגדרה)
conn = st.connection("gsheets", type=GSheetsConnection, spreadsheet="https://docs.google.com/spreadsheets/d/1-mrlAW07r7OIDhrW7-abdeF4fkySZzkODD4bEg6T7kg/edit?usp=sharing")

try:
    # קריאת הנתונים מהגיליון (ללא שמירה בזיכרון מטמון כדי שיתעדכן מיד)
    df = conn.read(ttl=0)
    df = df.dropna(how="all")
except Exception as e:
    # במקרה של שגיאה בקריאה, ניצור טבלה ריקה עם העמודות הנכונות
    df = pd.DataFrame(columns=["שם הספר", "שם המחבר", "מיקום"])

# --- תפריט צד להוספת ספר חדש ---
st.sidebar.header("➕ הוספת ספר חדש")
with st.sidebar.form("add_form", clear_on_submit=True):
    new_name = st.text_input("שם הספר")
    new_author = st.text_input("שם המחבר")
    new_loc = st.text_input("איפה הוא נמצא? (מדף/חדר)")
    
    submit = st.form_submit_button("הוסף לקטלוג")
    
    if submit:
        if new_name and new_author:
            # יצירת שורה חדשה וחיבור לטבלה הקיימת
            new_row = pd.DataFrame([{"שם הספר": new_name, "שם המחבר": new_author, "מיקום": new_loc}])
            updated_df = pd.concat([df, new_row], ignore_index=True)
            
            try:
                # פקודת העדכון ששולחת את המידע חזרה לגוגל שיטס
                conn.update(data=updated_df)
                st.sidebar.success(f"הספר '{new_name}' נוסף בהצלחה!")
                # ריענון האפליקציה כדי להציג את הספר החדש מיד
                st.rerun()
            except Exception as e:
                st.sidebar.error("שגיאה בעדכון הגיליון. ודאו שהגיליון מוגדר כ-'Editor' לכל מי שיש לו קישור.")
        else:
            st.sidebar.error("חובה למלא שם ספר ומחבר")

# --- חיפוש ותצוגה ---
st.write("---")
search = st.text_input("🔍 חפשו ספר, מחבר או מיקום:", placeholder="למשל: מאיר שלו, מדף א'...")

if search:
    # סינון הטבלה לפי מילת החיפוש
    mask = df.astype(str).apply(lambda x: x.str.contains(search, case=False, na=False)).any(axis=1)
    results = df[mask]
    
    if not results.empty:
        st.dataframe(results, use_container_width=True, hide_index=True)
    else:
        st.warning("לא מצאנו ספר כזה במאגר...")
else:
    # תצוגה של כל הספרים אם אין חיפוש פעיל
    if not df.empty:
        st.write("📖 **כל הספרים בקטלוג:**")
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("הקטלוג ריק כרגע. זה הזמן להוסיף את הספר הראשון!")

st.write("---")
st.caption(f"סה''כ ספרים רשומים: {len(df)}")
