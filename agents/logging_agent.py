import os
import json
import datetime
from crewai import Agent
from typing import Dict, Any

def create_logging_agent() -> Agent:
    """Create and configure the Logging Agent"""
    return Agent(
        role="Customer Interaction Data Analyst",
        goal="Accurately log and track all customer service interactions for analysis and improvement",
        backstory="""You are a meticulous data analyst specializing in customer service operations. 
        You understand the importance of comprehensive logging for improving service quality, 
        identifying trends, and ensuring compliance with customer service standards. Your detailed 
        records help the organization learn and improve.
        
        When logging an interaction, create a comprehensive record that includes:
        - Unique interaction ID with timestamp
        - Complete customer query and response details
        - Escalation decision and reasoning
        - Resolution status and analytics
        - Processing metadata for performance tracking
        
        Format your response as JSON with these fields:
        - logged: boolean (true/false)
        - interaction_id: unique identifier
        - timestamp: ISO format timestamp
        - analytics: summary of key metrics
        - log_location: where the data was stored
        """,
        verbose=True,
        allow_delegation=False
    )