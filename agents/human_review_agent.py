# agents/human_review_agent.py

def review_email(email: dict, response: str) -> str:
    """
    Simulates human review of the generated email response.
    Prints the response and prompts the user to decide if it should be modified.
    
    Argumentss:
        email (dict): The email being processed (can be used for context).
        response (str): The auto-generated response.
    
    Returns:
        str: The final response after human review.
        
    """
    print("\nGenerated Response:\n")
    print(response)
    
    user_input = input("\nDo you want to make any changes to the response? (y/n): ")
    if user_input.lower() == "y":
        modified_response = input("\nEnter the corrected response: ")
        return modified_response
    else:
        return response
