import os
import json
from crewai import Agent
from openai import OpenAI
from typing import Dict, Any

def process_faq_query(question: str) -> Dict[str, Any]:
    """
    Process customer questions using either mock responses or OpenAI API
    """
    mock_mode = os.getenv("MOCK_MODE", "true").lower() == "true"
    
    if mock_mode:
        return get_mock_response(question)
    else:
        return get_openai_response(question)

def get_mock_response(question: str) -> Dict[str, Any]:
    """
    Provide mock responses based on common FAQ patterns
    """
    question_lower = question.lower()
    
    # FAQ knowledge base patterns
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

def get_openai_response(question: str) -> Dict[str, Any]:
    """
    Get response from OpenAI API with FAQ context
    """
    try:
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        openai_key = os.getenv("OPENAI_API_KEY")
        if not openai_key:
            return get_mock_response(question)
            
        client = OpenAI(api_key=openai_key)
        
        faq_context = """
        You are a helpful customer service FAQ agent. Answer questions about:
        - Order status and tracking
        - Shipping and delivery
        - Returns and refunds
        - Account and login issues
        - Payment and billing
        
        Provide helpful, accurate responses. If you're not confident about an answer,
        indicate that the question should be escalated to a human agent.
        
        Respond in JSON format with: answer, confidence (0-1), and category.
        """
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": faq_context},
                {"role": "user", "content": f"Customer question: {question}"}
            ],
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        if content:
            return json.loads(content)
        else:
            return get_mock_response(question)
        
    except Exception as e:
        # Fallback to mock response if API fails
        return {
            "answer": "I'm experiencing technical difficulties. Please try again later or contact human support.",
            "confidence": 0.20,
            "category": "error",
            "error": str(e)
        }

def create_faq_agent() -> Agent:
    """
    Create and configure the FAQ Agent
    """
    return Agent(
        role="FAQ Customer Service Agent",
        goal="Answer frequently asked questions accurately and helpfully",
        backstory="""You are an experienced customer service representative with deep knowledge 
        of company policies, procedures, and common customer concerns. You excel at providing 
        quick, accurate answers to routine questions while identifying when issues need human intervention.""",
        verbose=True,
        allow_delegation=False
    )