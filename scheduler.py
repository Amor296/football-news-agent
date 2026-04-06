import pandas as pd
import schedule
import time
import os
from main import run_agent_workflow
from datetime import datetime

def morning_job():
    """
    Morning Execution: Runs every day at 09:00 AM.
    Delivers reports to all active subscribers using their saved language preference.
    """
    print(f"🌞 [Morning Task] Starting delivery at: {datetime.now()}")
    try:
        data_file = "data/subscribers.xlsx"
        if not os.path.exists(data_file):
            print("❌ Error: subscribers.xlsx not found.")
            return

        # Load the subscriber database
        df = pd.read_excel(data_file)
        
        for index, row in df.iterrows():
            # Process only active accounts
            if str(row['Status']).strip() == 'Active':
                print(f"📧 Sending {row['Language']} report to: {row['Email']}")
                
                # We pass Topic, Email, Interest, and the new Language parameter
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
    Evening Execution: Runs every day at 09:00 PM.
    Only delivers to users who selected the 'Twice Daily' schedule.
    """
    print(f"🌙 [Evening Task] Starting delivery at: {datetime.now()}")
    try:
        data_file = "data/subscribers.xlsx"
        if not os.path.exists(data_file):
            print("❌ Error: subscribers.xlsx not found.")
            return

        df = pd.read_excel(data_file)
        
        for index, row in df.iterrows():
            # Check for Active status and Twice Daily preference
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

# --- Precise Scheduling Configuration ---

# Task 1: Trigger Morning Dispatch at 09:00 AM
schedule.every().day.at("09:00").do(morning_job)

# Task 2: Trigger Evening Dispatch at 21:00 (09:00 PM)
schedule.every().day.at("21:00").do(evening_job)

print("--------------------------------------------------")
print("🚀 Football Insights Multi-Lingual Scheduler Active")
print(f"Current System Time: {datetime.now().strftime('%H:%M:%S')}")
print("Schedule: 09:00 AM (All) & 09:00 PM (Twice Daily)")
print("--------------------------------------------------")

# Keep-alive loop to monitor the schedule
while True:
    schedule.run_pending()
    # Check every 60 seconds to minimize CPU usage
    time.sleep(60)