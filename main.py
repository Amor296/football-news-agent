import os
from datetime import datetime
from groq import Groq
from tavily import TavilyClient
from tools.email_tools import send_news_email

# --- [STEP 1: API KEYS LOADING] ---
# This part checks Render Environment first, then falls back to local file
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

if not GROQ_API_KEY:
    try:
        # Falls back to your local config.py if not on Render
        import config 
        GROQ_API_KEY = config.GROQ_API_KEY
        TAVILY_API_KEY = config.TAVILY_API_KEY
        EMAIL_SENDER = config.EMAIL_SENDER
        EMAIL_PASSWORD = config.EMAIL_PASSWORD
        print("✅ Mode: Local Machine (Using config.py)")
    except ImportError:
        print("❌ CRITICAL ERROR: API Keys not found in Environment or config.py")
else:
    print("🚀 Mode: Render Cloud (Using Environment Variables)")

# --- [STEP 2: INITIALIZE CLIENTS] ---
groq_client = Groq(api_key=GROQ_API_KEY)
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

def get_comprehensive_news(topic, interest):
    """Fetches real-time 2026 data."""
    current_date = datetime.now().strftime("%d %B %Y")
    try:
        query = f"breaking {topic} {interest} news today {current_date} official"
        results = tavily_client.search(query=query, max_results=5, days=1)
        return results['results']
    except Exception as e:
        print(f"Tavily Error: {e}")
        return []

def generate_professional_report(topic, data_pool, language):
    """AI synthesis based on selected language."""
    current_year = datetime.now().year
    prompt = f"""
    ROLE: Senior Sports Journalist.
    LANGUAGE: Write EVERYTHING in {language.upper()}. 
    TARGET: Top 4 real football events from {current_year}.
    STRUCTURE:
    - [✅ CONFIRMED] or [⚠️ RUMOR] + **Bold Title**
    - 3 Deep sentences (Action, Context, Impact).
    - 📢 Source: [Website Name]
    - 🔗 Link: [URL]
    """
    try:
        completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": f"Factual sports bot in {language}. Temp 0.0."},
                {"role": "user", "content": prompt + f"\n\nDATA:\n{data_pool}"}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.0
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Groq Error: {e}")
        return None

def run_agent_workflow(topic, receiver_email, interest, language="English"):
    """Orchestrates the entire process."""
    data = get_comprehensive_news(topic, interest)
    if not data: return None
    
    report = generate_professional_report(topic, data, language)
    
    if report:
        subject = f"⚽ Precision Update: {topic} ({language})"
        # Passing credentials to the email tool
        success = send_news_email(receiver_email, subject, report)
        return report
    return None