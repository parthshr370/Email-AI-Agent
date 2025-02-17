# core/email_ingestion.py
import json
from pathlib import Path

def fetch_email(simulate: bool = True):
    """
    Fetches emails. If simulate=True, load emails from a JSON file.
    """
    if simulate:
        # Construct the path to the JSON file dynamically
        email_file = Path(__file__).parent.parent / "sample_emails.json"
        


        try:
            with open(email_file, "r") as f:
                emails = json.load(f)
            return emails
        except FileNotFoundError:
            print(f"Error: {email_file} not found. Ensure the JSON file is correctly placed.")
            return []
    else:
        # Implement IMAP/POP3 integration if needed
        return []



# addede implementation that reads the email from a JSON file
# added als the part wherre it reads the port number to make sure if runing locally