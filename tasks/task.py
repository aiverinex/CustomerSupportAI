from crewai import Task
from typing import Dict, Any

def create_faq_task(agent, customer_query: str) -> Task:
    """
    Create task for FAQ Agent to process customer query
    """
    return Task(
        description=f"""
        Process the following customer query and provide a helpful response:
        
        Customer Query: {customer_query}
        
        Analyze the customer's question and provide a response in JSON format with:
        - answer: A clear, helpful response to the customer's question
        - confidence: Your confidence level (0-1) in this response
        - category: The type of question (order_status, returns, shipping, account, billing, or unknown)
        
        Be helpful and professional in your response.
        """,
        agent=agent,
        expected_output="JSON response with answer, confidence score, and category"
    )

def create_escalation_task(agent, faq_response: str, customer_query: str) -> Task:
    """
    Create task for Escalation Agent to determine if human intervention is needed
    """
    return Task(
        description=f"""
        Analyze the FAQ response and customer query to determine if escalation is needed:
        
        Customer Query: {customer_query}
        FAQ Response: {faq_response}
        
        Determine if this interaction should be escalated to a human agent and provide your analysis in JSON format with:
        - escalate: true or false
        - reason: explanation for your decision
        - priority: "low", "normal", "high", or "urgent"
        - confidence_score: the FAQ confidence score from the response
        - category: the FAQ category from the response
        - human_agent_suggestion: "general_support", "technical", "billing", or "manager"
        
        Consider response confidence, emotional tone, complexity, and urgency indicators.
        """,
        agent=agent,
        expected_output="JSON escalation decision with reasoning, priority, and agent suggestion"
    )

def create_logging_task(agent, customer_query: str, faq_response: str, escalation_decision: str) -> Task:
    """
    Create task for Logging Agent to record the interaction
    """
    return Task(
        description=f"""
        Log the complete customer service interaction for tracking and analysis:
        
        Customer Query: {customer_query}
        FAQ Response: {faq_response}
        Escalation Decision: {escalation_decision}
        
        Create a comprehensive log entry in JSON format with:
        - logged: true or false
        - interaction_id: unique identifier with timestamp
        - timestamp: current timestamp in ISO format
        - analytics: summary of key metrics (escalated, confidence_score, category, etc.)
        - log_location: where the data was stored (e.g., "logs/customer_interactions.json")
        
        Generate analytics and provide confirmation of successful logging.
        """,
        agent=agent,
        expected_output="JSON confirmation of successful logging with interaction ID and analytics"
    )

def create_customer_support_workflow_task(faq_agent, escalation_agent, logging_agent, customer_query: str, user_id: str = "anonymous") -> list:
    """
    Create the complete workflow of tasks for processing a customer support request
    """
    # Task 1: FAQ Agent processes the query
    faq_task = Task(
        description=f"""
        Process customer query: "{customer_query}"
        
        Provide a helpful response using your FAQ knowledge base.
        Include confidence score and categorization.
        """,
        agent=faq_agent,
        expected_output="FAQ response with answer, confidence, and category"
    )
    
    # Task 2: Escalation Agent evaluates the response
    escalation_task = Task(
        description=f"""
        Evaluate if the customer query "{customer_query}" and its FAQ response 
        require escalation to human agents.
        
        Consider response confidence, query complexity, and customer satisfaction indicators.
        """,
        agent=escalation_agent,
        expected_output="Escalation decision with reasoning and priority",
        context=[faq_task]  # Depends on FAQ task output
    )
    
    # Task 3: Logging Agent records everything
    logging_task = Task(
        description=f"""
        Log the complete customer service interaction including:
        - Customer query: "{customer_query}"
        - User ID: {user_id}
        - FAQ response details
        - Escalation decision
        - Timestamps and metadata
        
        Create comprehensive records for analysis and tracking.
        """,
        agent=logging_agent,
        expected_output="Logging confirmation with interaction ID",
        context=[faq_task, escalation_task]  # Depends on both previous tasks
    )
    
    return [faq_task, escalation_task, logging_task]
