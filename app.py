import streamlit as st
import pandas as pd
import os
from main import run_agent_workflow

# --- 1. Page Configuration & UI Styling ---
st.set_page_config(page_title="2026 AI Football Agent", page_icon="⚽", layout="centered")

# Custom CSS for a professional Dark Mode look
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    .report-box { padding: 20px; border: 1px solid #30363d; border-radius: 10px; background-color: #161b22; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚽ Elite Football Insights (2026)")
st.subheader("Your AI-Powered Daily Football Intelligence")

# --- 2. Subscriber Data Management ---
data_file = "data/subscribers.xlsx"

# Ensure data directory and excel file exist
if not os.path.exists("data"):
    os.makedirs("data")

if not os.path.exists(data_file):
    # Initialize an empty DataFrame if file doesn't exist
    df = pd.DataFrame(columns=["Email", "Interest", "Language"])
    df.to_excel(data_file, index=False, engine='openpyxl')

# --- 3. User Interface (Sidebar & Form) ---
with st.form("subscription_form"):
    st.write("### 📧 Subscribe to Daily Reports")
    email = st.text_input("Enter your Email:")
    interest = st.selectbox("Favorite Team/League:", ["Real Madrid", "Premier League", "Egyptian League", "Al Ahly", "Zamalek", "Transfers"])
    language = st.radio("Report Language:", ["Arabic", "English"], horizontal=True)
    
    submit_button = st.form_submit_button("Subscribe & Get Instant Report")

# --- 4. Logic Processing on Submit ---
if submit_button:
    if email and "@" in email:
        # Load existing subscriber data
        current_data = pd.read_excel(data_file, engine='openpyxl')
        
        # Check if user is already in the system
        if email not in current_data['Email'].values:
            new_entry = pd.DataFrame([[email, interest, language]], columns=["Email", "Interest", "Language"])
            updated_data = pd.concat([current_data, new_entry], ignore_index=True)
            
            # CRITICAL: Using 'openpyxl' engine for cloud deployment compatibility
            updated_data.to_excel(data_file, index=False, engine='openpyxl')
            st.success(f"Successfully subscribed: {email}")
        else:
            st.info("You are already subscribed! Generating your instant report...")

        # Trigger AI Workflow immediately for the user
        with st.spinner("🤖 AI Agent is searching for 2026 football news..."):
            # run_agent_workflow returns the generated report string
            report = run_agent_workflow(interest, email, interest, language)
            
            if report:
                st.markdown("### 📄 Latest Report Preview:")
                # Display the AI report inside a styled div
                st.markdown(f"<div class='report-box'>{report}</div>", unsafe_allow_html=True)
                st.balloons()
            else:
                st.error("Could not generate report. Please verify your API Keys in Streamlit Secrets.")
    else:
        st.warning("Please enter a valid email address.")

# --- 5. Footer ---
st.markdown("---")
st.caption("Powered by Groq Llama 3.3 & Tavily Search | 2026 Season")