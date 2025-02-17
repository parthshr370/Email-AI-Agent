from langchain.prompts import PromptTemplate
from config import DEEPSEEK_API_KEY  # Import the key from your config
from langchain_openai import ChatOpenAI
from utils.formatter import clean_text



def summarize_email(email: dict) -> str:
    """
    Uses an LLM to generate a concise summary of the email content.
    """
    prompt_template = PromptTemplate(
        input_var=["content"],
        template="Summarize the following email content in 2 to 3 sentences: {content}"
    )
    
    prompt = prompt_template.format(content=email.get("body", ""))
    
    # Initialize the model with Deepseek's configurations
    model = ChatOpenAI(
        base_url="https://api.deepseek.com/v1",  # Deepseek's API endpoint
        model="deepseek-chat",
        temperature=0.3,
        openai_api_key=DEEPSEEK_API_KEY         # Your Deepseek API key (from .env)
    )
    
    summary = model.invoke(prompt)
    summary_text = summary.content if hasattr(summary, "content") else str(summary)
    
    
    return clean_text(summary_text)