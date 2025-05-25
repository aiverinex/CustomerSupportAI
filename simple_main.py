#!/usr/bin/env python3
"""
Simple Customer Support System Demo
"""

import os
import json
from datetime import datetime

# Simple FAQ response function
def get_faq_response(question):
    """Get FAQ response based on keywords"""
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

# Simple escalation decision
def should_escalate(faq_response, customer_query):
    """Determine if escalation is needed"""
    confidence = faq_response.get("confidence", 0.5)
    
    # Escalate if confidence is low
    if confidence < 0.6:
        return {
            "escalate": True,
            "reason": "Low confidence in automated response",
            "priority": "normal"
        }
    
    # Check for urgent keywords
    urgent_keywords = ["emergency", "urgent", "manager", "complaint", "terrible"]
    if any(keyword in customer_query.lower() for keyword in urgent_keywords):
        return {
            "escalate": True,
            "reason": "Query contains urgent keywords",
            "priority": "high"
        }
    
    return {
        "escalate": False,
        "reason": "Query resolved by automated system",
        "priority": "none"
    }

# Log interaction
def log_interaction(customer_query, faq_response, escalation_decision):
    """Log the customer interaction"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "customer_query": customer_query,
        "faq_response": faq_response,
        "escalation_decision": escalation_decision,
        "interaction_id": f"CS_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    }
    
    print(f"\n📝 INTERACTION LOGGED: {log_entry['interaction_id']}")
    return log_entry

def main():
    """Main customer support demo"""
    print("🎯 Customer Support Agent Crew Demo")
    print("=" * 50)
    
    # Load sample query
    sample_query = "Where is my order? I placed it 5 days ago and haven't received any tracking information."
    
    print(f"\n💬 Sample Customer Query:")
    print(f"   {sample_query}")
    
    # Step 1: FAQ Agent responds
    print(f"\n🤖 FAQ Agent Processing...")
    faq_response = get_faq_response(sample_query)
    print(f"   Answer: {faq_response['answer']}")
    print(f"   Confidence: {faq_response['confidence']}")
    print(f"   Category: {faq_response['category']}")
    
    # Step 2: Escalation Agent decides
    print(f"\n🎯 Escalation Agent Processing...")
    escalation_decision = should_escalate(faq_response, sample_query)
    if escalation_decision['escalate']:
        print(f"   🚨 ESCALATION NEEDED")
        print(f"   Reason: {escalation_decision['reason']}")
        print(f"   Priority: {escalation_decision['priority']}")
    else:
        print(f"   ✅ No escalation needed")
        print(f"   Reason: {escalation_decision['reason']}")
    
    # Step 3: Logging Agent records
    print(f"\n📊 Logging Agent Processing...")
    log_entry = log_interaction(sample_query, faq_response, escalation_decision)
    
    # Final summary
    print(f"\n✅ CUSTOMER SUPPORT WORKFLOW COMPLETE")
    print("=" * 50)
    print(f"Query processed successfully!")
    print(f"Resolution: {'Escalated to human' if escalation_decision['escalate'] else 'Resolved by bot'}")
    
    # Interactive mode
    print(f"\n🎮 Try your own question:")
    user_query = input("Enter your question: ").strip()
    
    if user_query:
        print(f"\n🔄 Processing your question...")
        user_faq = get_faq_response(user_query)
        user_escalation = should_escalate(user_faq, user_query)
        user_log = log_interaction(user_query, user_faq, user_escalation)
        
        print(f"\n💡 Response: {user_faq['answer']}")
        print(f"📊 Confidence: {user_faq['confidence']}")
        if user_escalation['escalate']:
            print(f"🚨 This query would be escalated to a human agent")
        else:
            print(f"✅ This query was resolved automatically")

if __name__ == "__main__":
    main()