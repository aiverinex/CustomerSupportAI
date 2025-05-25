#!/usr/bin/env python3
"""
Customer Support Agent Crew - Working Test Version
"""

import os
import json
from datetime import datetime

# Set mock mode for testing
os.environ["MOCK_MODE"] = "true"

def process_faq_query(question: str):
    """FAQ Agent - Process customer questions"""
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
    else:
        return {
            "answer": "I'm not sure about that specific question. Let me escalate this to a human agent who can better assist you.",
            "confidence": 0.30,
            "category": "unknown"
        }

def process_escalation_decision(faq_response, customer_query):
    """Escalation Agent - Determine if human intervention is needed"""
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
    
    # Complex query keywords
    urgent_keywords = ["emergency", "urgent", "manager", "complaint", "terrible", "frustrated"]
    if any(keyword in customer_query.lower() for keyword in urgent_keywords):
        escalation_needed = True
        escalation_reason = "Query contains urgent keywords"
        priority = "urgent"
    
    # Category-based escalation
    if category in ["unknown", "error"]:
        escalation_needed = True
        escalation_reason = "Unable to categorize query"
    
    return {
        "escalate": escalation_needed,
        "reason": escalation_reason,
        "priority": priority,
        "confidence_score": confidence,
        "category": category,
        "human_agent_suggestion": "general_support" if escalation_needed else "none"
    }

def log_interaction(customer_query, faq_response, escalation_decision):
    """Logging Agent - Record the interaction"""
    timestamp = datetime.now()
    interaction_id = f"CS_{timestamp.strftime('%Y%m%d_%H%M%S')}"
    
    log_entry = {
        "interaction_id": interaction_id,
        "timestamp": timestamp.isoformat(),
        "customer_query": customer_query,
        "faq_response": faq_response,
        "escalation_decision": escalation_decision,
        "resolution_status": "escalated" if escalation_decision["escalate"] else "resolved"
    }
    
    # Print to console (simulating logging)
    escalated = escalation_decision["escalate"]
    status_icon = "🚨" if escalated else "✅"
    
    print(f"\n{status_icon} INTERACTION LOGGED: {interaction_id}")
    print(f"Resolution: {log_entry['resolution_status']}")
    if escalated:
        print(f"Escalation Reason: {escalation_decision['reason']}")
        print(f"Priority: {escalation_decision['priority']}")
    
    return log_entry

def run_customer_support_workflow(customer_query):
    """Run the complete customer support workflow"""
    print(f"\n🎯 CUSTOMER SUPPORT WORKFLOW")
    print("=" * 50)
    print(f"Query: {customer_query}")
    
    # Step 1: FAQ Agent processes query
    print(f"\n🤖 FAQ Agent Processing...")
    faq_response = process_faq_query(customer_query)
    print(f"Answer: {faq_response['answer']}")
    print(f"Confidence: {faq_response['confidence']}")
    print(f"Category: {faq_response['category']}")
    
    # Step 2: Escalation Agent evaluates
    print(f"\n🎯 Escalation Agent Processing...")
    escalation_decision = process_escalation_decision(faq_response, customer_query)
    if escalation_decision['escalate']:
        print(f"🚨 ESCALATION NEEDED")
        print(f"Reason: {escalation_decision['reason']}")
        print(f"Priority: {escalation_decision['priority']}")
    else:
        print(f"✅ No escalation needed")
    
    # Step 3: Logging Agent records
    print(f"\n📊 Logging Agent Processing...")
    log_entry = log_interaction(customer_query, faq_response, escalation_decision)
    
    # Final summary
    print(f"\n✅ WORKFLOW COMPLETE")
    print("=" * 50)
    resolution = "Escalated to human agent" if escalation_decision['escalate'] else "Resolved automatically"
    print(f"Final Status: {resolution}")
    
    return {
        "success": True,
        "faq_response": faq_response,
        "escalation_decision": escalation_decision,
        "log_entry": log_entry
    }

def main():
    """Main demo function"""
    print("🎯 Customer Support Agent Crew - Test Demo")
    print("CrewAI Marketplace Compatible System")
    print("https://marketplace.crewai.com")
    
    # Test with sample queries
    test_queries = [
        "Where is my order? I placed it 5 days ago and haven't received any tracking information.",
        "I want to return a damaged product",
        "This is terrible service! I demand to speak to a manager immediately!",
        "How do I reset my password?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n\n{'='*60}")
        print(f"TEST {i}/{len(test_queries)}")
        run_customer_support_workflow(query)
    
    # Interactive mode
    print(f"\n\n{'='*60}")
    print("🎮 INTERACTIVE MODE")
    print("Enter your own customer support question:")
    
    user_query = input("\nYour question: ").strip()
    if user_query:
        run_customer_support_workflow(user_query)
    else:
        print("No question provided. Demo complete!")

if __name__ == "__main__":
    main()