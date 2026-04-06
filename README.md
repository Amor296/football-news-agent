# ⚽ Football Intelligence Cloud Agent (V1.0)

An advanced AI-powered sports journalism agent that delivers real-time, factual football reports directly to your email. Built for the 2026 season with a focus on zero-hallucination and high-impact news.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Cloud-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

An AI-powered football scouting agent that automates fan subscriptions and delivers personalized intelligence reports using Large Language Models (LLMs) and Google Sheets integration.

---

## 🚀 Live Demo
Experience the agent in action here:  
🔗 **[Football Intelligence App]((https://midan-football-news.streamlit.app/))

---

## ✨ Key Features
* **Smart Subscription System:** Seamlessly syncs user data (Team interest, Language, Schedule) to a Google Sheets database.
* **AI Scouting Reports:** Generates instant football analysis reports based on specific user interests using an autonomous agent workflow.
* **Secure Cloud Auth:** Implemented a robust **Base64-encoded PEM encryption** logic to handle Google Cloud Service Accounts securely on Streamlit Cloud.
* **Multi-language Support:** Delivers insights in both Arabic and English.
* **Clean UI:** Professional dark-themed dashboard built with Streamlit.

---

## 🛠️ Technical Stack
* **Frontend/App Framework:** [Streamlit](https://streamlit.io/)
* **Database Interface:** [Google Sheets API](https://developers.google.com/sheets/api) via `gspread`
* **Authentication:** Google Service Accounts (OAuth2)
* **Data Handling:** Pandas
* **AI Core:** LangChain / AI Agent Workflow (main.py)

---

📂 Project Structure
• agents/
   - researcher.py (AI Scout: Searches for latest football news & stats)
   - writer.py (AI Journalist: Crafts engaging reports in multiple languages)

• tools/
   - search_tools.py (Real-time web search integration via Serper/Google)
   - email_tools.py (Automated delivery system for sending reports)

• data/
   - processed/ (Storage for generated scouting reports & logs)

• .streamlit/
   - config.toml (UI Branding: Colors, fonts, and dark mode settings)
   - secrets.toml (Secure storage for API Keys & GSheets Base64)

• app.py (Main UI: Handles user registration and dashboard display)
• main.py (Core Orchestrator: Connects Agents with Tools)
• config.py (Global Settings: Model parameters and API endpoints)
• scheduler.py (Timing Logic: Manages automated delivery schedules)
• requirements.txt (List of all Python libraries needed for the project)
