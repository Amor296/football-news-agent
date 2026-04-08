import os
import threading
import time
import schedule  # Ensure 'schedule' is added to your requirements.txt
from datetime import datetime
from groq import Groq
from tavily import TavilyClient
from config import GROQ_API_KEY, TAVILY_API_KEY
from tools.email_tools import send_news_email

# Initialize API clients
groq_client = Groq(api_key=GROQ_API_KEY)
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

def get_comprehensive_news(topic, interest):
    """
    Fetches real-time news using Tavily Search API.
    """
    current_date = datetime.now().strftime("%d %B %Y")
    try:
        query = f"breaking {topic} {interest} news today {current_date} official"
        results = tavily_client.search(query=query, max_results=5, days=1)
        return results['results']
    except Exception as e:
        print(f"Tavily Error: {e}")
        return []

def generate_professional_report(topic, data_pool, language):
    """
    Synthesizes a journalistic report in the selected language using Groq Llama-3.
    """
    current_year = datetime.now().year
    
    # Define the persona and structure for the AI agent
    prompt = f"""
    ROLE: Senior Sports Journalist.
    LANGUAGE: Write EVERYTHING in {language.upper()}. 
    TARGET: Select the top 4 real football events from {current_year}.
    
    STRUCTURE:
    - [✅ CONFIRMED] or [⚠️ RUMOR] + **Bold Title**
    - 3 Informative sentences (Action, Context, Impact).
    - 📢 **Source:** [Website Name]
    - 🔗 **Link:** [Direct URL]
    """

    try:
        completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": f"You are a factual sports bot writing in {language}. Temperature 0.0 for accuracy."},
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
    """
    Orchestrates the full workflow: Search -> Research -> Write -> Email.
    """
    data = get_comprehensive_news(topic, interest)
    if not data: 
        print(f"No data found for {topic}")
        return None
    
    report = generate_professional_report(topic, data, language)
    
    if report:
        subject = f"Precision Update: {topic} ({language})"
        send_news_email(receiver_email, subject, report)
        return report
    return None

# --- NEW: Automated Scheduling Logic ---

def start_scheduler():
    """
    Background loop that checks for pending scheduled tasks.
    """
    def scheduled_task():
        print(f"Execution started at: {datetime.now()}")
        # Example: Triggering a specific report for a test user
        # In a real scenario, you can pull users/topics from a Database or Google Sheet here
        # run_agent_workflow("Real Madrid", "user@example.com", "Transfers", "Arabic")
        pass

    # Schedule the report to run at specific times (24h format)
    schedule.every().day.at("09:00").do(scheduled_task)
    schedule.every().day.at("21:00").do(scheduled_task)

    while True:
        schedule.run_pending()
        time.sleep(60) # Check for tasks every minute

def launch_background_scheduler():
    """
    Starts the scheduler in a separate thread to prevent blocking the Main UI/Process.
    """
    scheduler_thread = threading.Thread(target=start_scheduler, daemon=True)
    scheduler_thread.start()
    print("✅ Background Scheduler Engine Started!")

# Note: Call launch_background_scheduler() in your app.py to activate it.