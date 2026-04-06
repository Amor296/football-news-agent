import streamlit as st
import pandas as pd
import os
from datetime import datetime
from main import run_agent_workflow

# --- 1. Page Configuration & Professional Styling ---
st.set_page_config(page_title="Football Intelligence Pro", layout="centered")

# Custom CSS for a Clean, Premium Dark Interface
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background-color: #050505;
    }
    
    /* Premium Form Container */
    .stForm {
        background: #0f0f0f !important;
        padding: 30px !important;
        border-radius: 15px !important;
        border: 1px solid #1e1e1e !important;
    }
    
    /* Button Styling */
    .stButton>button {
        background: linear-gradient(90deg, #0062ff, #0047ba);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 8px;
        font-weight: bold;
        transition: 0.3s all;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,98,255,0.3);
    }
    
    /* Report Output Styling */
    .report-output {
        background-color: #0a0a0a;
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #222;
        line-height: 1.7;
        color: #d1d1d1;
        font-size: 1.05rem;
    }
    
    h1, h2, h3 { color: #ffffff !important; letter-spacing: -0.5px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. Data Initialization ---
data_file = "data/subscribers.xlsx"
if not os.path.exists("data"): os.makedirs("data")
if not os.path.exists(data_file):
    df = pd.DataFrame(columns=["Email", "Interest", "Language", "Preferred_Time", "Subscription_Date"])
    df.to_excel(data_file, index=False, engine='openpyxl')

# --- 3. UI Header ---
st.title("Football Intelligence")
st.write("Strategic Scouting & News Aggregation | 2026 Season")

# --- 4. Subscription Experience ---
with st.form("pro_subscription"):
    col1, col2 = st.columns(2)
    
    with col1:
        email = st.text_input("Professional Email", placeholder="user@domain.com")
        interest = st.selectbox("Intelligence Target", 
                              ["Real Madrid", "Premier League", "La Liga", "Egyptian League", "Al Ahly", "Zamalek", "Transfer Market"])
    
    with col2:
        language = st.selectbox("Report Language", ["English", "Arabic"])
        preferred_time = st.selectbox("Delivery Schedule", 
                                    ["Morning (09:00 AM)", "Evening (06:00 PM)", "Late Night (11:00 PM)", "Instant Only"])
    
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    submit_btn = st.form_submit_button("SYNC DATA & RUN")

# --- 5. Core Logic ---
if submit_btn:
    if email and "@" in email:
        # 1. Save or Update User Data in Excel
        current_data = pd.read_excel(data_file, engine='openpyxl')
        
        # Check if email exists to update or add new
        if email in current_data['Email'].values:
            # Update existing user preferences
            current_data.loc[current_data['Email'] == email, ['Interest', 'Language', 'Preferred_Time']] = [interest, language, preferred_time]
            updated_data = current_data
            status_msg = f"System Update: Preferences synchronized for {email}."
        else:
            # Add new subscriber
            new_entry = pd.DataFrame([[email, interest, language, preferred_time, datetime.now()]], 
                                   columns=["Email", "Interest", "Language", "Preferred_Time", "Subscription_Date"])
            updated_data = pd.concat([current_data, new_entry], ignore_index=True)
            status_msg = f"Identity Verified: {email} is now active."
        
        # Save changes to file
        updated_data.to_excel(data_file, index=False, engine='openpyxl')
        st.success(status_msg)

        # 2. Conditional Report Generation (ONLY for Instant Only)
        if preferred_time == "Instant Only":
            with st.spinner("Accessing global nodes for Instant Report..."):
                report = run_agent_workflow(interest, email, interest, language)
                
                if report:
                    st.markdown("### Latest Strategic Report")
                    st.markdown(f"<div class='report-output'>{report}</div>", unsafe_allow_html=True)
                    st.balloons()
                else:
                    st.error("Protocol Failure: Unable to fetch data. Check API configuration.")
        else:
            # Just show a scheduled confirmation
            st.info(f"Report Scheduled: You will receive your tactical intelligence at **{preferred_time}**.")
            st.warning("Immediate generation skipped based on your delivery preference.")
            
    else:
        st.error("Invalid Email: Identity verification failed.")

# --- 6. Institutional Footer ---
st.markdown("<br><hr style='border-color: #222;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #444; font-size: 0.75rem;'>2026 FOOTBALL INTELLIGENCE SYSTEM | ENCRYPTED DATA PIPE | NO EXTERNAL ICONS</p>", unsafe_allow_html=True)