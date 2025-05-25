import os
import json
from crewai import Agent
from openai import OpenAI
from typing import Dict, Any

def create_faq_agent() -> Agent:
    """Create and configure the FAQ Agent"""
    return Agent(
        role="FAQ Customer Service Agent",
        goal="Answer frequently asked questions accurately and helpfully",
        backstory="""You are an experienced customer service representative with deep knowledge 
        of company policies, procedures, and common customer concerns. You excel at providing 
        quick, accurate answers to routine questions while identifying when issues need human intervention.
        
        When a customer asks a question, analyze it and provide a helpful response. Always include:
        - A clear, helpful answer
        - Your confidence level (0-1) in the response
        - The category of the question (order_status, returns, shipping, account, billing, or unknown)
        
        Format your response as JSON with these fields: answer, confidence, category""",
        verbose=True,
        allow_delegation=False
    )