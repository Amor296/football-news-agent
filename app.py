import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
from main import run_agent_workflow

# --- 1. Page Configuration & Professional UI ---
st.set_page_config(page_title="Football Intelligence Cloud", layout="centered")

# Custom CSS for Premium Look (No Icons, Dark Mode)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #050505; }
    .stForm { 
        background: #0f0f0f !important; 
        padding: 30px !important; 
        border-radius: 15px !important; 
        border: 1px solid #1e1e1e !important; 
    }
    .stButton>button { 
        background: linear-gradient(90deg, #0062ff, #0047ba); 
        color: white; 
        border: none;
        border-radius: 8px; 
        width: 100%; 
        font-weight: bold; 
        text-transform: uppercase;
    }
    .report-output { 
        background-color: #0a0a0a; 
        padding: 25px; 
        border-radius: 12px; 
        border: 1px solid #222; 
        color: #d1d1d1; 
        line-height: 1.7; 
    }
    h1, h2, h3 { color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. Cloud Connection (Google Sheets) ---
# It uses the [connections.gsheets] section from your Streamlit Secrets
conn = st.connection("gsheets", type=GSheetsConnection)

def get_data():
    # ttl=0 ensures we don't use cached/old data
    # We specify 'Sheet1' which is the default tab name in Google Sheets
    return conn.read(worksheet="Sheet1", ttl=0)

# --- 3. UI Header ---
st.title("Football Intelligence")
st.write("Strategic Scouting & News Aggregation | Cloud-Synced")

# --- 4. Subscription Experience ---
with st.form("pro_subscription"):
    col1, col2 = st.columns(2)
    with col1:
        email = st.text_input("Professional Email", placeholder="user@domain.com")
        interest = st.selectbox("Intelligence Target", ["Real Madrid", "Premier League", "La Liga", "Egyptian League", "Al Ahly", "Zamalek", "Transfer Market"])
    with col2:
        language = st.selectbox("Report Language", ["English", "Arabic"])
        preferred_time = st.selectbox("Delivery Schedule", ["Morning (09:00 AM)", "Evening (06:00 PM)", "Late Night (11:00 PM)", "Instant Only"])
    
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    submit_btn = st.form_submit_button("SYNC TO CLOUD & RUN")

# --- 5. Core Logic (GSheets Update & Report) ---
if submit_btn:
    if email and "@" in email:
        try:
            # 1. Fetch Fresh Data
            df = get_data()
            
            # Clean empty rows
            df = df.dropna(how="all")

            # 2. Check & Update or Append
            if not df.empty and email in df['Email'].values:
                df.loc[df['Email'] == email, ['Interest', 'Language', 'Preferred_Time']] = [interest, language, preferred_time]
                status_msg = f"Cloud Preferences Updated for {email}."
            else:
                new_entry = pd.DataFrame([[email, interest, language, preferred_time, datetime.now().strftime("%Y-%m-%d %H:%M:%S")]], 
                                       columns=["Email", "Interest", "Language", "Preferred_Time", "Subscription_Date"])
                df = pd.concat([df, new_entry], ignore_index=True)
                status_msg = f"New Identity Registered: {email} is now in the cloud database."
            
            # 3. Push back to Google Sheets (Targeting Sheet1)
            conn.update(worksheet="Sheet1", data=df)
            st.success(status_msg)

            # 4. Instant Report Logic
            if preferred_time == "Instant Only":
                with st.spinner("Processing Real-time Node Search..."):
                    report = run_agent_workflow(interest, email, interest, language)
                    if report:
                        st.markdown("### Strategic Report")
                        st.markdown(f"<div class='report-output'>{report}</div>", unsafe_allow_html=True)
                        st.balloons()
                    else:
                        st.error("Protocol Error: Unable to generate report. Check API keys.")
            else:
                st.info(f"Protocol Scheduled: Intelligence will be dispatched at **{preferred_time}**.")
                
        except Exception as e:
            st.error(f"Cloud Connection Failed: Ensure the sheet is shared with your Service Account and Secrets are correct.")
            st.info("Technical Detail: " + str(e))
    else:
        st.error("Identity Verification Failed: Please provide a valid professional email.")

# --- 6. Institutional Footer ---
st.markdown("<br><hr style='border-color: #222;'><p style='text-align: center; color: #444; font-size: 0.75rem;'>2026 CLOUD INTELLIGENCE SYSTEM | SECURE DATA PIPE</p>", unsafe_allow_html=True)