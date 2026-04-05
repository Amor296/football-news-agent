import pandas as pd
from datetime import datetime
from main import run_agent_workflow
import os

def start_scheduling():
    data_file = "data/subscribers.xlsx"
    if not os.path.exists(data_file):
        print("No subscribers found.")
        return

    df = pd.read_excel(data_file)
    current_hour = datetime.now().hour # get current hour to determine which subscribers to send to based on their preferred times 
    
    # range for morning, afternoon, evening based on the times we set in the app
    time_tag = ""
    if 7 <= current_hour <= 10: time_tag = "morning"
    elif 14 <= current_hour <= 17: time_tag = "afternoon"
    elif 19 <= current_hour <= 22: time_tag = "evening"

    print(f"⏰ Checking for subscribers for: {time_tag}")

    for _, row in df.iterrows():
        # Printing for debugging purposes - to see which subscribers are being process and their preferred times
        if time_tag in str(row['Preferred Times']) and row['Status'] == 'Active':
            print(f"📧 Sending to {row['Email']} about {row['Topic']}...")
            run_agent_workflow(row['Topic'], row['Email'])

if __name__ == "__main__":
    start_scheduling()