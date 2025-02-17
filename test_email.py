from core.email_sender import send_email

test_email = {
    "from": "recipient@example.com",  # Replace with a valid recipient email
    "subject": "Test Email",
    "response": "Hello, this is a test email from the AI Email Assistant!"
}

if send_email(test_email):
    print("Test email sent successfully!")
else:
    print("Failed to send test email.")
