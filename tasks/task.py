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
        
        Your task is to:
        1. Analyze the customer's question
        2. Provide an accurate and helpful response based on FAQ knowledge
        3. Assign a confidence score to your response (0-1)
        4. Categorize the query type
        
        Return your response in a structured format that includes the answer, 
        confidence score, and category.
        """,
        agent=agent,
        expected_output="Structured response with answer, confidence score, and category"
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
        
        Your task is to:
        1. Evaluate the quality and completeness of the FAQ response
        2. Assess the complexity and emotional tone of the customer query
        3. Determine if human intervention is required
        4. If escalation is needed, specify the reason and priority level
        5. Suggest the appropriate type of human agent
        
        Consider factors like:
        - Response confidence level
        - Query complexity
        - Emotional indicators
        - Keywords suggesting urgency or legal issues
        - Whether the FAQ response adequately addresses the customer's concern
        """,
        agent=agent,
        expected_output="Escalation decision with reasoning, priority, and agent type suggestion"
    )

def create_logging_task(agent, interaction_data: Dict[str, Any]) -> Task:
    """
    Create task for Logging Agent to record the interaction
    """
    return Task(
        description=f"""
        Log the complete customer service interaction for tracking and analysis:
        
        Interaction Data: {interaction_data}
        
        Your task is to:
        1. Create a comprehensive log entry with unique ID and timestamp
        2. Store all relevant interaction details
        3. Determine resolution status
        4. Generate analytics summary
        5. Save to the logging system
        6. Provide confirmation of successful logging
        
        Ensure all data is properly structured for future analysis and reporting.
        Include metadata about processing, agent versions, and system configuration.
        """,
        agent=agent,
        expected_output="Confirmation of successful logging with interaction ID and analytics summary"
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
