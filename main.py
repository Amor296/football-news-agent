# Import the agents
from agents.researcher import get_football_news
from agents.writer import write_news_article
# Import the email tool from the tools folder
from tools.email_tools import send_news_email

def run_agent_workflow(topic, user_email):
    """
    The main coordinator that runs the search, writing, and emailing process.
    This function is called directly by app.py (Streamlit).
    """
    
    # --- Step 1: Research Phase ---
    # Fetch data using the researcher agent (Tavily)
    search_data = get_football_news(topic)
    
    # --- Step 2: Data Preparation ---
    # Combine search results into a context string for the writer
    # Using 'content' or 'raw_content' to provide more details to the AI
    detailed_context = ""
    for res in search_data['results']:
        title = res.get('title', 'No Title')
        snippet = res.get('content', '')
        detailed_context += f"\n- {title}: {snippet}\n"
    
    # --- Step 3: Writing Phase ---
    # Generate the professional Arabic report using the writer agent (Groq)
    print(f"✍️  Generating report for: {topic}...")
    final_article = write_news_article(topic, detailed_context)
    
    # --- Step 4: Emailing Phase ---
    # Send the final report to the user's email
    if user_email:
        print(f"📧 Sending email to: {user_email}...")
        subject = f"⚽ تقريرك الرياضي: {topic}"
        
        # Add links to the email body for reference
        links_text = "\n\n🔗 المصادر:\n" + "\n".join([res['url'] for res in search_data['results']])
        email_body = final_article + links_text
        
        # Call the tool we created in tools/email_tools.py
        success = send_news_email(user_email, subject, email_body)
        
        if success:
            print("✅ Email sent successfully!")
        else:
            print("❌ Failed to send email. Check your config/App Password.")

    # Return the article so Streamlit can display it on the screen
    return final_article

if __name__ == "__main__":
    # This part allows you to still test the file directly from the terminal
    test_topic = "آخر أخبار الدوري الإنجليزي"
    test_email = "your-test-email@example.com" # Change this to your real email to test
    print(run_agent_workflow(test_topic, test_email))