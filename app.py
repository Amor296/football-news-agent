import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
from main import run_agent_workflow

# --- 1. Page Configuration & UI Styling ---
st.set_page_config(page_title="Football Intelligence Cloud", layout="centered")

# Custom CSS for a professional dark theme
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
SHEET_URL = "https://docs.google.com/spreadsheets/d/1cpSclVF8-KngIfZjxxokhAV1NLIxQSbDu_EYhZH1PPc/edit"

def get_fixed_secrets():
    """
    Retrieves and fixes the Google Service Account private key format
    to prevent 'Unable to load PEM file' errors in cloud environments.
    """
    try:
        # Load credentials from Streamlit Secrets
        creds = dict(st.secrets["connections"]["gsheets"])
        if "private_key" in creds:
            # Replace escaped newlines with actual newline characters
            creds["private_key"] = creds["private_key"].replace("\\n", "\n")
        return creds
    except Exception as e:
        st.error("Secrets Configuration Missing! Please check Streamlit Cloud Settings.")
        return None

# Initialize connection with fixed credentials
fixed_creds = get_fixed_secrets()

if fixed_creds:
    conn = st.connection("gsheets", type=GSheetsConnection, **fixed_creds)
else:
    st.stop() # Halt execution if secrets are unavailable

def get_data():
    """Fetches the latest data from the specified Google Sheet."""
    return conn.read(spreadsheet=SHEET_URL, worksheet="Sheet1", ttl=0)

# --- 3. UI Header ---
st.title("Football Intelligence")
st.write("Cloud-Synced Strategic Scouting | 2026 Season")

# --- 4. User Subscription Form ---
with st.form("pro_subscription"):
    col1, col2 = st.columns(2)
    with col1:
        email = st.text_input("Professional Email", placeholder="user@domain.com")
        interest = st.selectbox("Target Entity", ["Real Madrid", "Premier League", "La Liga", "Egyptian League", "Al Ahly", "Zamalek", "Transfer Market"])
    with col2:
        language = st.selectbox("Intelligence Language", ["English", "Arabic"])
        preferred_time = st.selectbox("Delivery Schedule", ["Morning (09:00 AM)", "Evening (06:00 PM)", "Late Night (11:00 PM)", "Instant Only"])
    
    submit_btn = st.form_submit_button("SYNC TO CLOUD & RUN")

# --- 5. Core Logic: Data Sync & Agent Execution ---
if submit_btn:
    if email and "@" in email:
        try:
            # Step A: Fetch existing data from the Cloud
            df = get_data()
            df = df.dropna(how="all")

            # Step B: Logic to either Update existing user or Append new record
            if not df.empty and email in df['Email'].values:
                df.loc[df['Email'] == email, ['Interest', 'Language', 'Preferred_Time']] = [interest, language, preferred_time]
                status_msg = f"Cloud Preferences Updated for {email}."
            else:
                new_entry = pd.DataFrame([[email, interest, language, preferred_time, datetime.now().strftime("%Y-%m-%d %H:%M:%S")]], 
                                       columns=["Email", "Interest", "Language", "Preferred_Time", "Subscription_Date"])
                df = pd.concat([df, new_entry], ignore_index=True)
                status_msg = f"New Identity Registered: {email}."
            
            # Step C: Push the updated DataFrame back to Google Sheets
            conn.update(spreadsheet=SHEET_URL, worksheet="Sheet1", data=df)
            st.success(status_msg)

            # Step D: Trigger AI Agent Workflow if 'Instant Only' is selected
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
            st.error("Critical Cloud Error. Check your connection or sheet permissions.")
            st.exception(e) 
    else:
        st.error("Invalid Email: Verification failed.")

# --- 6. Institutional Footer ---
st.markdown("<br><hr style='border-color: #222;'><p style='text-align: center; color: #444; font-size: 0.75rem;'>2026 CLOUD INTELLIGENCE SYSTEM | DATA SYNC ACTIVE</p>", unsafe_allow_html=True)