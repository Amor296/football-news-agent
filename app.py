import streamlit as st
import pandas as pd
import os
from main import run_agent_workflow

# Page Config
st.set_page_config(page_title="Elite Football Insights", page_icon="⚽", layout="wide")

# Custom CSS for Dark Sports Theme
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3.5em; background-color: #1f77b4; color: white; font-weight: bold; border: none; }
    .report-box { background-color: #1e1e26; padding: 25px; border-radius: 12px; border-left: 6px solid #1f77b4; margin-top: 20px; color: #e0e0e0; }
    </style>
    """, unsafe_allow_html=True)

st.title("Elite Football Insights")
st.markdown("### Professional AI Sports Analyst at your service")

# Organizing UI in Columns
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("#### 👤 User Profile")
    user_email = st.text_input("Your Email Address")
    topic = st.text_input("Target Topic (Team/Player)")
    
    # NEW: Language Selector
    report_lang = st.selectbox("Report Language", ["English", "Arabic"])

with col2:
    st.markdown("#### Preferences")
    interest = st.selectbox("Intelligence Type", ["General News", "Transfer Market", "Match Analysis"])
    delivery_pref = st.radio("Delivery Schedule:", [
        "Morning Report (09:00 AM)", 
        "Twice Daily (AM/PM)",
        "Instant Report (Run Now)"
    ])

st.divider()

if st.button("Activate Intelligence"):
    if user_email and topic:
        with st.spinner(f"Processing {report_lang} Intelligence for {topic}..."):
            # 1. Save to Excel (Including Language)
            data_dir = "data"
            if not os.path.exists(data_dir): os.makedirs(data_dir)
            data_file = os.path.join(data_dir, "subscribers.xlsx")
            
            new_data = pd.DataFrame([{
                "Email": user_email, 
                "Topic": topic, 
                "Language": report_lang, # Saved for scheduler
                "Interest": interest, 
                "Schedule": delivery_pref, 
                "Status": "Active"
            }])
            
            if not os.path.isfile(data_file):
                new_data.to_excel(data_file, index=False)
            else:
                df = pd.read_excel(data_file)
                pd.concat([df, new_data]).drop_duplicates(subset=['Email'], keep='last').to_excel(data_file, index=False)

            # 2. Immediate Run Logic
            if "Instant" in delivery_pref:
                # We pass 'report_lang' to the workflow
                report = run_agent_workflow(topic, user_email, interest, report_lang)
                if report:
                    st.success(f"Success! {report_lang} report generated.")
                    st.markdown(f'<div class="report-box">{report}</div>', unsafe_allow_html=True)
                else:
                    st.error("No verified data found for today.")
            else:
                st.success(f"Subscription Confirmed! Your {report_lang} reports will start at the scheduled time.")
    else:
        st.warning("Please provide both email and a topic.")