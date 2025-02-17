import smtplib
from email.mime.text import MIMEText
from config import EMAIL_SERVER, EMAIL_PASSWORD, EMAIL_USERNAME, EMAIL_PORT
from email.message import EmailMessage
from utils.logger import get_logger
from utils.formatter import clean_text,format_email
import os




"""
Use this function if you want to change to a local  file saving behavio for drafts 

        
also change the for loop for the main function to -  

        # Check if a response was generated
        if "response" in email:
            # Ask the user if they want to send the email or save it as a draft
            action = input("Do you want to (s)end the email or save it as a (d)raft? (s/d): ").strip().lower()
            if action == "s":
                if send_email(email, user_name):
                    logger.info("Email sent successfully.")
                else:
                    logger.warning("Failed to send email.")
            elif action == "d":
                if save_draft(email, user_name):
                    logger.info("Draft saved successfully.")
                else:
                    logger.warning("Failed to save draft.")
            else:
                logger.warning("Invalid option. No action taken.")
        
        
        
        """


logger = get_logger(__name__)

def extract_name_from_email(email_address: str) -> str:
    """
    Extracts the portion before the '@' as a friendly name.
    """
    if "@" in email_address:
        return email_address.split("@")[0]
    return email_address




def send_draft_to_gmail(email: dict, user_name: str, gmail_address: str) -> bool:
    try:
        subject = clean_text(email.get("subject", ""))
        # Use .strip() to preserve newlines in the response content
        raw_response_content = email.get("response", "").strip()
        recipient_email = gmail_address  # Use the provided Gmail address as the recipient
        sender_name = extract_name_from_email(email.get("from", "Unknown"))
        
        # Format the email content
        response_content = format_email(subject, sender_name, raw_response_content, user_name)
        
        msg = EmailMessage()
        msg["Subject"] = f"Draft: Re: {subject}"
        msg["From"] = EMAIL_USERNAME
        msg["To"] = recipient_email
        msg.set_content(response_content)
        
        logger.debug("Connecting to SMTP server %s:%s for sending draft", EMAIL_SERVER, EMAIL_PORT)
        with smtplib.SMTP(EMAIL_SERVER, int(EMAIL_PORT)) as server:
            logger.debug("Starting TLS for draft sending...")
            server.starttls()
            logger.debug("Logging in as %s", EMAIL_USERNAME)
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            logger.debug("Sending draft email to %s", recipient_email)
            server.send_message(msg)
            logger.info("Draft sent to Gmail account at %s", recipient_email)
        
        return True
    except Exception as e:
        logger.error("Failed to send draft to Gmail: %s", e)
        return False





def send_email(email: dict, user_name: str) -> bool:
    """
    Sends an email reply via SMTP using the generated response.
    """
    try:
        subject = clean_text(email.get("subject", ""))
        raw_response_content = email.get("response", "").strip()  # don't collapse newlines
        recipient_email = email.get("from", "")
        sender_name = extract_name_from_email(recipient_email)
        
        # Use the updated format_email which preserves body line breaks
        response_content = format_email(subject, sender_name, raw_response_content, user_name)
        
        msg = EmailMessage()
        msg["Subject"] = f"Re: {subject}"
        msg["From"] = EMAIL_USERNAME
        msg["To"] = recipient_email
        msg.set_content(response_content)
        
        logger.debug("Connecting to SMTP server %s:%s", EMAIL_SERVER, EMAIL_PORT)
        with smtplib.SMTP(EMAIL_SERVER, int(EMAIL_PORT)) as server:
            logger.debug("Starting TLS...")
            server.starttls()
            logger.debug("Logging in as %s", EMAIL_USERNAME)
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            logger.debug("Sending email to %s", recipient_email)
            server.send_message(msg)
            logger.info("Email sent to %s", recipient_email)
        
        return True
    except Exception as e:
        logger.error("Failed to send email: %s", e)
        return False
    
