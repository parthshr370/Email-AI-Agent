# core/email_imap.py
import imaplib
import email
from email.header import decode_header

def fetch_imap_emails(username, password, imap_server="imap.gmail.com"):
    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(username, password)
    mail.select("inbox")
    status, messages = mail.search(None, "ALL")
    email_ids = messages[0].split()
    emails = []
    for num in email_ids:
        status, msg_data = mail.fetch(num, "(RFC822)")
        raw_email = msg_data[0][1] # The entire email message is a byte string
        msg = email.message_from_bytes(raw_email)
        subject, encoding = decode_header(msg.get("Subject"))[0] # Decode the email subject
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else "utf-8")
        emails.append({ # Extract the email ID, sender, subject, and body
            "id": num.decode(),
            "from": msg.get("From"),
            "subject": subject,
            "body": extract_email_body(msg)
        })
    mail.logout()
    return emails

def extract_email_body(msg):
    if msg.is_multipart(): # The email body may be in multiple parts
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            if content_type == "text/plain" and "attachment" not in content_disposition:
                charset = part.get_content_charset() or "utf-8"
                return part.get_payload(decode=True).decode(charset, errors="replace")
    else:
        charset = msg.get_content_charset() or "utf-8"
        return msg.get_payload(decode=True).decode(charset, errors="replace")
