from langchain.prompts import PromptTemplate
from config import DEEPSEEK_API_KEY  # Import the key from your config
from langchain_openai import ChatOpenAI

from utils.formatter import clean_text, format_email


from email.utils import parseaddr


def generate_response(email: dict, summary: str, recipient_name: str, your_name: str) -> str:
    prompt_template = PromptTemplate(
        input_variables=["sender", "subject", "content", "summary", "user_name","recipient_name"],
        template=(
            "You are an email assistant. Do not use placeholders like [User's Name]"
            "You are an email assistant. Do not include any greeting or signature lines in your response.\n\n"
            "Email Details:\n"
            "From: {sender}\n"
            "Subject: {subject}\n"
            "Content: {content}\n"
            "Summary: {summary}\n\n"
            
            "Reply in a formal tone."
        )
    )
    
    prompt = prompt_template.format(
        sender=recipient_name,  # Use the recipient's name (supplied manually)
        subject=email.get("subject", ""),
        content=email.get("body", ""),
        summary=summary,
        user_name=your_name
    )
    
    model = ChatOpenAI(
        base_url="https://api.deepseek.com/v1",
        model="deepseek-chat",
        temperature=0.5,
        openai_api_key=DEEPSEEK_API_KEY
    )
    
    response = model.invoke(prompt)
    response_text = response.content if hasattr(response, "content") else str(response)
    
    # Pass recipient_name (for greeting) and your_name (for signature)
    formatted_response = format_email(email.get("subject", ""), recipient_name, response_text, your_name)
    return formatted_response.strip()
