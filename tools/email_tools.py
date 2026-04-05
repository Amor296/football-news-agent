import smtplib
from email.message import EmailMessage
# Importing credentials from your central config file
from config import EMAIL_SENDER, EMAIL_PASSWORD 

def send_news_email(receiver_email, subject, body):
    """
    Sends an email using Gmail's SMTP server.
    :param receiver_email: The email address of the recipient.
    :param subject: The subject line of the email.
    :param body: The main content (news article) of the email.
    :return: True if sent successfully, False otherwise.
    """
    
    # Create the email message object
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_SENDER
    msg['To'] = receiver_email

    try:
        # Standard Gmail SMTP settings for SSL (Port 465)
        # Using a context manager 'with' ensures the connection closes automatically
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            # Authenticate using the App Password from your .env/config
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            
            # Send the actual message
            smtp.send_message(msg)
            
        print(f"📧 Success: Email sent to {receiver_email}")
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("❌ Auth Error: Check your EMAIL_SENDER and App Password in .env")
        return False
    except Exception as e:
        print(f"❌ Error sending email: {str(e)}")
        return False