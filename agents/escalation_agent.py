import os
import json
from crewai import Agent
from openai import OpenAI
from typing import Dict, Any

def create_escalation_agent() -> Agent:
    """Create and configure the Escalation Agent"""
    return Agent(
        role="Escalation Decision Specialist",
        goal="Intelligently determine when customer queries require human intervention",
        backstory="""You are a seasoned customer service supervisor with years of experience 
        in managing complex customer situations. You have an excellent ability to assess 
        when automated responses are sufficient versus when human empathy, expertise, 
        or authority is needed to resolve customer concerns effectively.
        
        When analyzing a customer query and FAQ response, determine if escalation is needed based on:
        - Response confidence level (escalate if below 0.6)
        - Emotional tone or urgency in the customer's message
        - Complexity of the query
        - Keywords that suggest legal, billing, or technical issues
        - Whether the FAQ response adequately addresses the concern
        
        Format your response as JSON with these fields:
        - escalate: boolean (true/false)
        - reason: explanation for the decision
        - priority: "low", "normal", "high", or "urgent"
        - confidence_score: the FAQ confidence score
        - category: the FAQ category
        - human_agent_suggestion: "general_support", "technical", "billing", or "manager"
        """,
        verbose=True,
        allow_delegation=False
    )