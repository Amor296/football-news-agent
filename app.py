import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
import base64
from main import run_agent_workflow

# --- 1. Page Configuration ---
st.set_page_config(page_title="Football Intelligence Cloud", layout="centered")

# --- 2. Secure Cloud Connection Logic ---
SHEET_ID = "1cpSclVF8-KngIfZjxxokhAV1NLIxQSbDu_EYhZH1PPc"

def get_gspread_client():
    try:
        # Step 1: Copy secrets to a dictionary to allow modification
        creds_info = dict(st.secrets["connections"]["gsheets"])
        
        # Step 2: Handle Private Key (Support both Base64 and Normal text)
        raw_key = creds_info["private_key"]
        
        if not raw_key.startswith("-----"):
            # If key is Base64 encoded, decode it back to PEM format
            decoded_key = base64.b64decode(raw_key).decode("utf-8")
            creds_info["private_key"] = decoded_key
        else:
            # If key is normal text, ensure newlines are handled correctly
            creds_info["private_key"] = raw_key.replace("\\n", "\n")
        
        # Step 3: Define scopes and authenticate
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = Credentials.from_service_account_info(creds_info, scopes=scopes)
        return gspread.authorize(creds)
        
    except Exception as e:
        st.error(f"Authentication Failed: {str(e)}")
        return None

# Initialize the Google Sheets Client
client = get_gspread_client()

def get_data():
    if client:
        try:
            sheet = client.open_by_key(SHEET_ID).sheet1
            data = sheet.get_all_records()
            return pd.DataFrame(data)
        except Exception as e:
            st.error(f"Error fetching data: {e}")
    return pd.DataFrame()

def update_data(df):
    if client:
        try:
            sheet = client.open_by_key(SHEET_ID).sheet1
            sheet.clear()
            # Update sheet with headers and data
            sheet.update([df.columns.values.tolist()] + df.values.tolist())
            return True
        except Exception as e:
            st.error(f"Error updating sheet: {e}")
    return False

# --- 3. UI Styling ---
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

# --- 4. Subscription Form ---
with st.form("subscription_form"):
    col1, col2 = st.columns(2)
    with col1:
        email = st.text_input("Email Address")
        interest = st.selectbox("Team/League Interest", ["Real Madrid", "Al Ahly", "Zamalek", "Premier League"])
    with col2:
        language = st.selectbox("Preferred Language", ["English", "Arabic"])
        pref_time = st.selectbox("Delivery Schedule", ["Morning", "Evening", "Instant Only"])
    
    submit = st.form_submit_button("SYNC & RUN ANALYSIS")

# --- 5. Application Logic ---
if submit:
    if email and "@" in email:
        df = get_data()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Check if user already exists
        if not df.empty and email in df['Email'].values:
            df.loc[df['Email'] == email, ['Interest', 'Language', 'Preferred_Time']] = [interest, language, pref_time]
            status_msg = "Account synchronized successfully!"
        else:
            # Add new user record
            new_row = pd.DataFrame([[email, interest, language, pref_time, now]], 
                                 columns=["Email", "Interest", "Language", "Preferred_Time", "Subscription_Date"])
            df = pd.concat([df, new_row], ignore_index=True)
            status_msg = "Welcome! Your scouting profile is created."
        
        # Push to Google Sheets
        if update_data(df):
            st.success(status_msg)
            
            # Execute AI Workflow if Instant is selected
            if pref_time == "Instant Only":
                with st.spinner("Agent is analyzing football data..."):
                    report = run_agent_workflow(interest, email, interest, language)
                    st.markdown(f"<div class='report-output'>{report}</div>", unsafe_allow_html=True)
    else:
        st.error("Please provide a valid email address.")