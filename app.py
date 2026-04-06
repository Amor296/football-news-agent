import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
from main import run_agent_workflow

# --- 1. Page Configuration & UI ---
st.set_page_config(page_title="Football Intelligence Cloud", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #050505; }
    .stForm { background: #0f0f0f !important; padding: 30px !important; border-radius: 15px !important; border: 1px solid #1e1e1e !important; }
    .stButton>button { background: linear-gradient(90deg, #0062ff, #0047ba); color: white; border-radius: 8px; width: 100%; font-weight: bold; }
    .report-output { background-color: #0a0a0a; padding: 25px; border-radius: 12px; border: 1px solid #222; color: #d1d1d1; line-height: 1.7; }
    h1, h2, h3 { color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. Cloud Connection (Google Sheets) ---
# رابط الشيت بتاعك مباشرة
SHEET_URL = "https://docs.google.com/spreadsheets/d/1cpSclVF8-KngIfZjxxokhAV1NLIxQSbDu_EYhZH1PPc/edit#gid=0"

conn = st.connection("gsheets", type=GSheetsConnection)

def get_data():
    # بنمرر الرابط هنا مباشرة عشان نتفادى خطأ "Spreadsheet must be specified"
    return conn.read(spreadsheet=SHEET_URL, worksheet="Sheet1", ttl=0)

# --- 3. UI Header ---
st.title("Football Intelligence")
st.write("Cloud-Synced Strategic Scouting | 2026 Season")

# --- 4. Subscription Form ---
with st.form("pro_subscription"):
    col1, col2 = st.columns(2)
    with col1:
        email = st.text_input("Professional Email", placeholder="user@domain.com")
        interest = st.selectbox("Target Entity", ["Real Madrid", "Premier League", "La Liga", "Egyptian League", "Al Ahly", "Zamalek", "Transfer Market"])
    with col2:
        language = st.selectbox("Intelligence Language", ["English", "Arabic"])
        preferred_time = st.selectbox("Delivery Schedule", ["Morning (09:00 AM)", "Evening (06:00 PM)", "Late Night (11:00 PM)", "Instant Only"])
    
    submit_btn = st.form_submit_button("SYNC TO CLOUD & RUN")

# --- 5. Core Logic (GSheets Sync) ---
if submit_btn:
    if email and "@" in email:
        try:
            # Fetch data using the direct URL
            df = get_data()
            df = df.dropna(how="all")

            if not df.empty and email in df['Email'].values:
                df.loc[df['Email'] == email, ['Interest', 'Language', 'Preferred_Time']] = [interest, language, preferred_time]
                status_msg = f"Cloud Preferences Updated for {email}."
            else:
                new_entry = pd.DataFrame([[email, interest, language, preferred_time, datetime.now().strftime("%Y-%m-%d %H:%M:%S")]], 
                                       columns=["Email", "Interest", "Language", "Preferred_Time", "Subscription_Date"])
                df = pd.concat([df, new_entry], ignore_index=True)
                status_msg = f"New Identity Registered: {email}."
            
            # التحديث باستخدام الرابط المباشر أيضاً
            conn.update(spreadsheet=SHEET_URL, worksheet="Sheet1", data=df)
            st.success(status_msg)

            if preferred_time == "Instant Only":
                with st.spinner("Processing Real-time Node Search..."):
                    report = run_agent_workflow(interest, email, interest, language)
                    if report:
                        st.markdown("### Strategic Report")
                        st.markdown(f"<div class='report-output'>{report}</div>", unsafe_allow_html=True)
                        st.balloons()
            else:
                st.info(f"Report Scheduled for: {preferred_time}")
                
        except Exception as e:
            st.error(f"Cloud Connection Failed: Check if the sheet is shared with the Service Account.")
            st.exception(e) # هيظهرلك الخطأ بالتفصيل عشان نعرف لو فيه حاجة تانية
    else:
        st.error("Invalid Email: Verification failed.")

st.markdown("<br><hr style='border-color: #222;'><p style='text-align: center; color: #444; font-size: 0.75rem;'>2026 CLOUD INTELLIGENCE SYSTEM</p>", unsafe_allow_html=True)