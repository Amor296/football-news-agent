import pandas as pd
import os
import time
from datetime import datetime
from main import run_agent_workflow

def morning_job():
    """
    Morning Execution: Runs once when triggered.
    Delivers reports to ALL active subscribers.
    """
    print(f"🌞 [Morning Task] Starting delivery at: {datetime.now()}")
    try:
        data_file = "data/subscribers.xlsx"
        if not os.path.exists(data_file):
            print(f"❌ Error: {data_file} not found.")
            return

        # Load the subscriber database
        df = pd.read_excel(data_file)
        
        for index, row in df.iterrows():
            # Process only active accounts
            if str(row['Status']).strip() == 'Active':
                print(f"📧 Sending {row['Language']} report to: {row['Email']}")
                
                run_agent_workflow(
                    topic=row['Topic'], 
                    receiver_email=row['Email'], 
                    interest=row['Interest'], 
                    language=row['Language']
                )
    except Exception as e:
        print(f"❌ Morning Job Critical Error: {e}")

def evening_job():
    """
    Evening Execution: Runs once when triggered.
    Only delivers to users who selected 'Twice Daily'.
    """
    print(f"🌙 [Evening Task] Starting delivery at: {datetime.now()}")
    try:
        data_file = "data/subscribers.xlsx"
        if not os.path.exists(data_file):
            print(f"❌ Error: {data_file} not found.")
            return

        df = pd.read_excel(data_file)
        
        for index, row in df.iterrows():
            is_active = str(row['Status']).strip() == 'Active'
            is_twice_daily = "Twice Daily" in str(row['Schedule'])
            
            if is_active and is_twice_daily:
                print(f"📧 Sending evening {row['Language']} report to: {row['Email']}")
                
                run_agent_workflow(
                    topic=row['Topic'], 
                    receiver_email=row['Email'], 
                    interest=row['Interest'], 
                    language=row['Language']
                )
    except Exception as e:
        print(f"❌ Evening Job Critical Error: {e}")

# --- GitHub Actions Logic: Runs once per trigger ---

def run_now():
    """
    Decides which job to run based on the current system hour (UTC).
    GitHub Actions will trigger this script at 07:00 and 19:00 UTC.
    """
    current_hour = datetime.now().hour
    print(f"Current System Hour (UTC): {current_hour}")

    # GitHub Action Cron '0 7 * * *' triggers around hour 7
    if 5 <= current_hour <= 11:
        morning_job()
    
    # GitHub Action Cron '0 19 * * *' triggers around hour 19
    elif 17 <= current_hour <= 23:
        evening_job()
    
    else:
        # If triggered manually from GitHub Actions UI
        print("Triggered manually or outside cron windows. Defaulting to morning_job...")
        morning_job()

if __name__ == "__main__":
    print("--------------------------------------------------")
    print("🚀 Football Insights Automation Script Active")
    print("--------------------------------------------------")
    run_now()
    print("--------------------------------------------------")
    print("✅ Task Completed. System shutting down.")