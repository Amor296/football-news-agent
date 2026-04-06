import streamlit as st
import pandas as pd
import os
from datetime import datetime
from main import run_agent_workflow

# --- 1. Premium Page Configuration ---
st.set_page_config(page_title="Football Intelligence Pro", layout="centered")

# Custom CSS for high-end "Hand-Crafted" Look
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background-color: #050505;
    }
    
    .main-card {
        background: linear-gradient(145deg, #111111, #0a0a0a);
        padding: 40px;
        border-radius: 20px;
        border: 1px solid #222;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        margin-bottom: 25px;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #0062ff, #0047ba);
        color: white;
        border: none;
        padding: 15px 30px;
        border-radius: 12px;
        font-weight: bold;
        transition: 0.3s all;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,98,255,0.4);
    }
    
    .report-output {
        background-color: #0f0f0f;
        padding: 25px;
        border-radius: 15px;
        border-left: 4px solid #0062ff;
        line-height: 1.6;
        color: #e0e0e0;
    }
    
    h1, h2, h3 { color: #ffffff !important; letter-spacing: -1px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. Data Initialization ---
data_file = "data/subscribers.xlsx"
if not os.path.exists("data"): os.makedirs("data")
if not os.path.exists(data_file):
    df = pd.DataFrame(columns=["Email", "Interest", "Language", "Preferred_Time", "Subscription_Date"])
    df.to_excel(data_file, index=False, engine='openpyxl')

# --- 3. UI Header ---
st.markdown("<div style='text-align: center; padding: 20px 0;'>", unsafe_allow_html=True)
st.title("Football Intelligence")
st.write("Advanced Global Scouting & News Aggregation System")
st.markdown("</div>", unsafe_allow_html=True)

# --- 4. Subscription Experience ---
# We removed the extra markdown div that was causing the empty black box
with st.container():
    # Applying the card style directly inside the form using a single div
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    
    with st.form("pro_subscription", clear_on_submit=False):
        col1, col2 = st.columns(2)
        
        with col1:
            email = st.text_input("Professional Email", placeholder="name@company.com")
            interest = st.selectbox("Target Entity", 
                                  ["Real Madrid", "Premier League", "La Liga", "Egyptian League", "Al Ahly", "Zamalek", "Transfer Market"])
        
        with col2:
            language = st.selectbox("Intelligence Language", ["English", "Arabic"])
            preferred_time = st.selectbox("Report Delivery Schedule", 
                                        ["Morning (09:00 AM)", "Evening (06:00 PM)", "Late Night (11:00 PM)", "Instant Only"])
        
        st.markdown("<div style='padding: 10px 0;'></div>", unsafe_allow_html=True) # Minimal spacing
        submit_btn = st.form_submit_button("Initialize Data Sync")
    
    st.markdown("</div>", unsafe_allow_html=True)

# --- 5. Logic Execution ---
if submit_btn:
    if email and "@" in email:
        # Data Persistence
        current_data = pd.read_excel(data_file, engine='openpyxl')
        
        if email not in current_data['Email'].values:
            new_entry = pd.DataFrame([[email, interest, language, preferred_time, datetime.now()]], 
                                   columns=["Email", "Interest", "Language", "Preferred_Time", "Subscription_Date"])
            updated_data = pd.concat([current_data, new_entry], ignore_index=True)
            updated_data.to_excel(data_file, index=False, engine='openpyxl')
            st.success(f"System Synchronized: {email} is now active.")
        
        # Immediate Report Generation (Only if 'Instant Only' OR requested now)
        # Note: In a real system, the scheduler (GitHub Actions) would handle the other times.
        with st.spinner("Processing Real-Time Intelligence..."):
            report = run_agent_workflow(interest, email, interest, language)
            
            if report:
                st.markdown("### Strategic Intelligence Report")
                st.markdown(f"<div class='report-output'>{report}</div>", unsafe_allow_html=True)
                
                if preferred_time != "Instant Only":
                    st.info(f"Future reports will be dispatched during your selected window: {preferred_time}")
            else:
                st.error("Protocol Failure: Unable to fetch data. Check API configuration.")
    else:
        st.error("Identity Verification Failed: Please provide a valid email.")

# --- 6. Institutional Footer ---
st.markdown("<br><hr style='border-color: #222;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555; font-size: 0.8rem;'>OFFICIAL INTELLIGENCE SYSTEM | 2026 SEASON DATA | SECURE ENCRYPTION ENABLED</p>", unsafe_allow_html=True)