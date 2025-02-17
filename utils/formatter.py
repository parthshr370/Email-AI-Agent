from jinja2 import Template

def clean_text(text: str)-> str:
    """Remove extra whitespace and unwanted newlines."""
    return " ".join(text.split())


def format_email(subject: str, sender_name: str, body: str, user_name: str) -> str:
    cleaned_subject = clean_text(subject)
    cleaned_sender = clean_text(sender_name)
    cleaned_user = clean_text(user_name)
    cleaned_body = body.strip()
    
    # Remove a leading "Subject:" header if present
    if cleaned_body.lower().startswith("subject:"):
        lines = cleaned_body.splitlines()
        cleaned_body = "\n".join(lines[1:]).strip()
    
    # Remove duplicate signature if it already exists in the body.
    signature_marker = "Best regards,"
    if signature_marker in cleaned_body:
        cleaned_body = cleaned_body.split(signature_marker)[0].strip()
    
    formatted_email = (
        f"Subject: Re: {cleaned_subject}\n\n"
        f"Hi {cleaned_sender},\n\n"
        f"{cleaned_body}\n\n"
        f"Best regards,\n"
        f"{cleaned_user}"
    )
    return formatted_email
