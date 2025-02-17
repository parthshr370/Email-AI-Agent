from core.state import EmailState
from agents import filtering_agent, summarization_agent, response_agent, human_review_agent
from langgraph.graph import START , END, StateGraph

"""Originally, each node function was written to expect two parameters—an email and a state.
However, the LangGraph framework is designed to pass only one argument (the state) to each node."""

# Bringing all the states together with a supervisor helps to manage the flow of the email processing.
def supervisor_langgraph(email: dict, state: EmailState,user_name : str,recipient_name:str) -> EmailState:
    """
    Processes an individual email using a LangGraph workflow.
    Each step (filtering, summarization, response generation) is a node.
    Conditional edges are used to exit early for spam or to continue processing.
    """
    
    state.current_email = email
    
    def filtering_node(state: EmailState) -> EmailState:
        current_email = state.current_email
        print('filtering node started for email id : %s' % current_email.get("id", "unknown"))
        classification = filtering_agent.filter_email(current_email)
        current_email["classification"] = classification
        state.metadata[current_email.get("id", "unknown")] = classification
        return state

    
    def summarization_node(state: EmailState) -> EmailState:
        email = state.current_email
        summary = summarization_agent.summarize_email(email)
        email["summary"] = summary
        return state
    
    def response_node(state: EmailState) -> EmailState:
        email = state.current_email
        response = response_agent.generate_response(email, email.get("summary", ""),recipient_name,user_name) # The response agent uses the summary to generate a response.
        # If the classification indicates review or the response is uncertain, let a human intervene
        if email.get("classification") == "needs_review" or "?" in response:
            response = human_review_agent.review_email(email, response)
        email["response"] = response
        state.history.append({
            "email_id": email.get("id", "unkonwn"),
            "response": response
        })
        return state
    
    graph_builder = StateGraph(EmailState)     # now building tther graph from all the states 

    
    # addimng the nodes in the graph 
    graph_builder.add_node("filtering", filtering_node)
    graph_builder.add_node("summarization", summarization_node)
    graph_builder.add_node("response", response_node)
    
    
    
    
    
    
    # building conditional wortking with filtering now that it is not spam if spam then dustbin is the way 
    def post_filtering(state_update: EmailState):
        email = state.current_email
        if email.get("classification") == "spam":
            return END
        else:
            return "summarization"
    
    graph_builder.add_conditional_edges("filtering", post_filtering, {"summarization": "summarization", END: END})
    
    # This creates a direct edge (connection) from the "summarization" node to the "response" node.
    # if reaches summary node then must move to response node
    graph_builder.add_edge("summarization", "response")
    
    graph_builder.add_edge("response", END) # if respone comes then end to all please
    
    # Set the entry point to the filtering node.
    graph_builder.set_entry_point("filtering")
    
    # Compile the graph.
    graph = graph_builder.compile()
    
    # Invoke the graph with the current state.
    final_state = graph.invoke(state)
    return final_state
