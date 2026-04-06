import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
from main import run_agent_workflow

# --- 1. Page Configuration ---
st.set_page_config(page_title="Football Intelligence Cloud", layout="centered")

# --- 2. Manual Cloud Connection (The Bulletproof Way) ---
SHEET_ID = "1cpSclVF8-KngIfZjxxokhAV1NLIxQSbDu_EYhZH1PPc"

def get_gspread_client():
    try:
        # 1. Get credentials from secrets
        creds_info = st.secrets["connections"]["gsheets"]
        
        # 2. Fix the private key (The most common cause of failure)
        if "private_key" in creds_info:
            creds_info["private_key"] = creds_info["private_key"].replace("\\n", "\n")
        
        # 3. Define scopes and authorize
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = Credentials.from_service_account_info(creds_info, scopes=scopes)
        return gspread.authorize(creds)
    except Exception as e:
        st.error(f"Authentication Failed: {str(e)}")
        return None

# Initialize Client
client = get_gspread_client()

def get_data():
    if client:
        # Open by ID is much safer than URL
        sheet = client.open_by_key(SHEET_ID).sheet1
        data = sheet.get_all_records()
        return pd.DataFrame(data)
    return pd.DataFrame()

def update_data(df):
    if client:
        sheet = client.open_by_key(SHEET_ID).sheet1
        sheet.clear()
        # Prepare data including header
        sheet.update([df.columns.values.tolist()] + df.values.tolist())
        return True
    return False

# --- 3. UI & Styles ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: white; }
    .stForm { background: #0f0f0f !important; padding: 30px !important; border-radius: 15px !important; border: 1px solid #1e1e1e !important; }
    .stButton>button { background: linear-gradient(90deg, #0062ff, #0047ba); color: white; width: 100%; font-weight: bold; }
    .report-output { background-color: #0a0a0a; padding: 25px; border-radius: 12px; border: 1px solid #222; color: #d1d1d1; }
    </style>
    """, unsafe_allow_html=True)

st.title("Football Intelligence")
st.write("Professional Scouting Cloud | 2026")

# --- 4. Form ---
with st.form("subscription_form"):
    col1, col2 = st.columns(2)
    with col1:
        email = st.text_input("Email")
        interest = st.selectbox("Interest", ["Real Madrid", "Al Ahly", "Zamalek", "Premier League"])
    with col2:
        language = st.selectbox("Language", ["English", "Arabic"])
        pref_time = st.selectbox("Schedule", ["Morning", "Evening", "Instant Only"])
    
    submit = st.form_submit_button("SYNC & RUN")

# --- 5. Logic ---
if submit:
    if email and "@" in email:
        df = get_data()
        
        # Add timestamp
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if not df.empty and email in df['Email'].values:
            df.loc[df['Email'] == email, ['Interest', 'Language', 'Preferred_Time']] = [interest, language, pref_time]
            msg = "Account Updated!"
        else:
            new_row = pd.DataFrame([[email, interest, language, pref_time, now]], 
                                 columns=["Email", "Interest", "Language", "Preferred_Time", "Subscription_Date"])
            df = pd.concat([df, new_row], ignore_index=True)
            msg = "New Account Created!"
        
        if update_data(df):
            st.success(msg)
            if pref_time == "Instant Only":
                with st.spinner("Analyzing..."):
                    report = run_agent_workflow(interest, email, interest, language)
                    st.markdown(f"<div class='report-output'>{report}</div>", unsafe_allow_html=True)
    else:
        st.error("Check your email format")