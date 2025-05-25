"""
Simple Customer Support Agents - CrewAI Compatible
Fixed version that works with current CrewAI structure
"""

import os
import json
from datetime import datetime
from crewai import Agent
from openai import OpenAI
from typing import Dict, Any

def faq_agent_function(question: str) -> Dict[str, Any]:
    """FAQ Agent function - processes customer questions"""
    mock_mode = os.getenv("MOCK_MODE", "true").lower() == "true"
    
    if not mock_mode and os.getenv("OPENAI_API_KEY"):
        try:
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful customer service FAQ agent. Respond in JSON format with answer, confidence (0-1), and category."},
                    {"role": "user", "content": f"Customer question: {question}"}
                ],
                response_format={"type": "json_object"}
            )
            content = response.choices[0].message.content
            if content:
                return json.loads(content)
        except Exception:
            pass  # Fall back to mock mode
    
    # Mock responses
    question_lower = question.lower()
    
    if any(keyword in question_lower for keyword in ["order", "where is", "tracking", "status"]):
        return {
            "answer": "Your order is currently being processed. You can track your order using the tracking number sent to your email. Orders typically take 3-5 business days to arrive.",
            "confidence": 0.85,
            "category": "order_status"
        }
    elif any(keyword in question_lower for keyword in ["return", "refund", "exchange"]):
        return {
            "answer": "You can return items within 30 days of purchase. Please visit our returns portal or contact customer service with your order number for assistance.",
            "confidence": 0.90,
            "category": "returns"
        }
    elif any(keyword in question_lower for keyword in ["shipping", "delivery", "when will"]):
        return {
            "answer": "Standard shipping takes 3-5 business days. Express shipping takes 1-2 business days. Free shipping is available on orders over $50.",
            "confidence": 0.88,
            "category": "shipping"
        }
    elif any(keyword in question_lower for keyword in ["account", "login", "password", "email"]):
        return {
            "answer": "For account issues, please use the 'Forgot Password' link on the login page or contact our support team at support@company.com.",
            "confidence": 0.82,
            "category": "account"
        }
    elif any(keyword in question_lower for keyword in ["payment", "billing", "charge", "card"]):
        return {
            "answer": "We accept all major credit cards and PayPal. If you see an unexpected charge, please contact our billing department immediately.",
            "confidence": 0.85,
            "category": "billing"
        }
    else:
        return {
            "answer": "I'm not sure about that specific question. Let me escalate this to a human agent who can better assist you.",
            "confidence": 0.30,
            "category": "unknown"
        }

def escalation_agent_function(faq_response: Dict[str, Any], customer_query: str) -> Dict[str, Any]:
    """Escalation Agent function - determines if human intervention needed"""
    confidence = faq_response.get("confidence", 0.5)
    category = faq_response.get("category", "unknown")
    
    escalation_needed = False
    escalation_reason = ""
    priority = "normal"
    
    # Low confidence threshold
    if confidence < 0.6:
        escalation_needed = True
        escalation_reason = "Low confidence in automated response"
        priority = "high"
    
    # Complex keywords requiring human attention
    urgent_keywords = ["emergency", "urgent", "manager", "complaint", "terrible", "frustrated", "angry", "legal"]
    if any(keyword in customer_query.lower() for keyword in urgent_keywords):
        escalation_needed = True
        escalation_reason = "Query contains urgent keywords requiring human attention"
        priority = "urgent"
    
    # Category-based escalation
    if category in ["unknown", "error"]:
        escalation_needed = True
        escalation_reason = "Unable to categorize or process query"
    
    return {
        "escalate": escalation_needed,
        "reason": escalation_reason,
        "priority": priority,
        "confidence_score": confidence,
        "category": category,
        "human_agent_suggestion": "technical" if "technical" in customer_query.lower() else "general_support"
    }

def logging_agent_function(customer_query: str, faq_response: Dict[str, Any], escalation_decision: Dict[str, Any]) -> Dict[str, Any]:
    """Logging Agent function - records interaction"""
    timestamp = datetime.now()
    interaction_id = f"CS_{timestamp.strftime('%Y%m%d_%H%M%S')}_{hash(customer_query) % 10000:04d}"
    
    log_entry = {
        "interaction_id": interaction_id,
        "timestamp": timestamp.isoformat(),
        "customer_query": customer_query,
        "faq_response": faq_response,
        "escalation_decision": escalation_decision,
        "resolution_status": "escalated" if escalation_decision["escalate"] else "resolved"
    }
    
    # Console logging
    escalated = escalation_decision["escalate"]
    status_icon = "🚨" if escalated else "✅"
    print(f"\n{status_icon} INTERACTION LOGGED: {interaction_id}")
    print(f"Resolution: {log_entry['resolution_status']}")
    if escalated:
        print(f"Escalation: {escalation_decision['reason']} (Priority: {escalation_decision['priority']})")
    
    return {
        "logged": True,
        "interaction_id": interaction_id,
        "timestamp": timestamp.isoformat(),
        "log_entry": log_entry
    }

def create_faq_agent() -> Agent:
    """Create FAQ Agent"""
    return Agent(
        role="FAQ Customer Service Agent",
        goal="Answer frequently asked questions accurately and helpfully",
        backstory="You are an experienced customer service representative with deep knowledge of company policies and procedures.",
        verbose=True,
        allow_delegation=False
    )

def create_escalation_agent() -> Agent:
    """Create Escalation Agent"""
    return Agent(
        role="Escalation Decision Specialist", 
        goal="Intelligently determine when customer queries require human intervention",
        backstory="You are a seasoned customer service supervisor with excellent judgment about when human intervention is needed.",
        verbose=True,
        allow_delegation=False
    )

def create_logging_agent() -> Agent:
    """Create Logging Agent"""
    return Agent(
        role="Customer Interaction Data Analyst",
        goal="Accurately log and track all customer service interactions",
        backstory="You are a meticulous data analyst who ensures comprehensive logging for service improvement.",
        verbose=True,
        allow_delegation=False
    )