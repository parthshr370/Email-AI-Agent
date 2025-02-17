"""from agents import filtering_agent, summarization_agent, response_agent, human_review_agent
from langgraph.graph import START , END, StateGraph
from core.email_imap import fetch_imap_emails
from core.email_sender import send_email,send_draft_to_gmail
from utils.logger import get_logger
from config import IMAP_USERNAME, IMAP_PASSWORD, IMAP_SERVER
from core.supervisor import supervisor_langgraph 
from agents.response_agent import extract_name_from_email


logger = get_logger(__name__)

# main.py
from core.email_ingestion import fetch_email
from core.state import EmailState
from core.supervisor import supervisor_langgraph
from core.email_sender import send_email

# this one lets you chose if you want to draft or not 

def process_email_action(email, user_name):
    action = input("Do you want to (s)end the email or (d)raft it to Gmail? (s/d): ").strip().lower()
    if action == "s":
        if send_email(email, user_name):
            logger.info("Email sent successfully.")
        else:
            logger.warning("Failed to send email.")
    elif action == "d":
        # Ask for Gmail address only if drafting
        gmail_address = input("Please enter your Gmail address for drafts: ")
        if send_draft_to_gmail(email, user_name, gmail_address):
            logger.info("Draft sent to Gmail successfully.")
        else:
            logger.warning("Failed to send draft to Gmail.")
    else:
        logger.warning("Invalid option. No action taken.")




def main():
    logger.info("Starting main function.")
    
    user_name = extract_name_from_email(IMAP_USERNAME)
    
    # Use IMAP to fetch live emails
    emails = fetch_imap_emails(IMAP_USERNAME, IMAP_PASSWORD, IMAP_SERVER)
    logger.debug(f"Fetched {len(emails)} emails from IMAP.")
    
    if not emails:
        logger.info("No emails found.")
        return
    
    latest_emails = emails[-5:]  # get the last 5 emails from the inbox
    

    print("\nSelect an email to process:")
    for idx, email in enumerate(latest_emails):
        print(f"{idx + 1}. {email['subject']}")
    
    choice = int(input("Enter the number of the email you want to choose: ")) - 1
    if choice < 0 or choice >= len(latest_emails):
        print("Invalid choice. Exiting.")
        return
    
    selected_email = latest_emails[choice]
    
    # Create state and process the email through the workflow
    state = EmailState()
    state.emails = [selected_email]
    state.current_email = selected_email
    state = supervisor_langgraph(selected_email, state, user_name)
    
    print("\nGenerated Response:\n")
    print(selected_email.get("response", "No response generated."))
    
    changes = input("Do you want to make changes to the response? (y/n): ").strip().lower()
    if changes == "y":
        modified_response = input("Enter the modified response: ")
        selected_email["response"] = modified_response
    
    # Now process the final action (send vs. draft)
    process_email_action(selected_email, user_name)
    
    logger.info("All emails processed.")
    logger.debug(f"Final State: {state}")

if __name__ == "__main__":
    main()
"""


from agents import filtering_agent, summarization_agent, response_agent, human_review_agent
from langgraph.graph import START, END, StateGraph
from core.email_imap import fetch_imap_emails
from core.email_sender import send_email, send_draft_to_gmail
from utils.logger import get_logger
from config import IMAP_USERNAME, IMAP_PASSWORD, IMAP_SERVER
from core.supervisor import supervisor_langgraph
from core.state import EmailState


logger = get_logger(__name__)

def process_email_action(email, your_name):
    action = input("Do you want to (s)end the email or (d)raft it to Gmail? (s/d): ").strip().lower()
    if action == "s":
        if send_email(email, your_name):
            logger.info("Email sent successfully.")
        else:
            logger.warning("Failed to send email.")
    elif action == "d":
        gmail_address = input("Please enter your Gmail address for drafts: ")
        if send_draft_to_gmail(email, your_name, gmail_address):
            logger.info("Draft sent to Gmail successfully.")
        else:
            logger.warning("Failed to send draft to Gmail.")
    else:
        logger.warning("Invalid option. No action taken.")

def main():
    logger.info("Starting main function.")
    
    # Prompt for your own name (for signature) and for the recipient's name.
    your_name = input("Please enter your name (for signature): ")
    recipient_name = input("Please enter the recipient's name: ")
    
    # Use IMAP to fetch live emails
    emails = fetch_imap_emails(IMAP_USERNAME, IMAP_PASSWORD, IMAP_SERVER)
    logger.debug(f"Fetched {len(emails)} emails from IMAP.")
    
    if not emails:
        logger.info("No emails found.")
        return
    
    latest_emails = emails[-5:]
    
    print("\nSelect an email to process:")
    for idx, email in enumerate(latest_emails):
        print(f"{idx + 1}. {email['subject']}")
    
    choice = int(input("Enter the number of the email you want to choose: ")) - 1
    if choice < 0 or choice >= len(latest_emails):
        print("Invalid choice. Exiting.")
        return
    
    selected_email = latest_emails[choice]
    
    # Create state and process the email through the workflow
    state = EmailState()
    state.emails = [selected_email]
    state.current_email = selected_email
    # Pass your signature (your_name) to the supervisor pipeline
    state = supervisor_langgraph(selected_email, state, your_name,recipient_name)
    
    print("\nGenerated Response:\n")
    print(selected_email.get("response", "No response generated."))
    
    changes = input("Do you want to make changes to the response? (y/n): ").strip().lower()
    if changes == "y":
        modified_response = input("Enter the modified response: ")
        selected_email["response"] = modified_response
    
    # Now process the final action (send vs. draft)
    process_email_action(selected_email, your_name)
    
    logger.info("All emails processed.")
    logger.debug(f"Final State: {state}")

if __name__ == "__main__":
    main()
