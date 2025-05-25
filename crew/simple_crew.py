"""
Customer Support Crew - CrewAI Compatible Implementation
"""

import time
from datetime import datetime
from crewai import Crew, Task, Process
from agents.simple_agents import (
    create_faq_agent,
    create_escalation_agent, 
    create_logging_agent,
    faq_agent_function,
    escalation_agent_function,
    logging_agent_function
)
from typing import Dict, Any

class CustomerSupportCrew:
    """CrewAI-based customer support automation system"""
    
    def __init__(self):
        """Initialize the customer support crew with all agents"""
        self.faq_agent = create_faq_agent()
        self.escalation_agent = create_escalation_agent()
        self.logging_agent = create_logging_agent()
    
    def process_customer_query(self, customer_query: str, user_id: str = "anonymous") -> Dict[str, Any]:
        """Process a customer query through the complete support workflow"""
        start_time = time.time()
        
        try:
            print(f"\n🎯 Processing Customer Query: {customer_query}")
            print(f"👤 User ID: {user_id}")
            print(f"📅 Timestamp: {datetime.now().isoformat()}")
            print("=" * 60)
            
            # Step 1: FAQ Agent processes the query
            print(f"\n🤖 FAQ Agent Processing...")
            faq_response = faq_agent_function(customer_query)
            print(f"Answer: {faq_response['answer']}")
            print(f"Confidence: {faq_response['confidence']}")
            print(f"Category: {faq_response['category']}")
            
            # Step 2: Escalation Agent evaluates
            print(f"\n🎯 Escalation Agent Processing...")
            escalation_decision = escalation_agent_function(faq_response, customer_query)
            if escalation_decision['escalate']:
                print(f"🚨 ESCALATION NEEDED")
                print(f"Reason: {escalation_decision['reason']}")
                print(f"Priority: {escalation_decision['priority']}")
            else:
                print(f"✅ No escalation needed")
            
            # Step 3: Logging Agent records
            print(f"\n📊 Logging Agent Processing...")
            logging_result = logging_agent_function(customer_query, faq_response, escalation_decision)
            
            processing_time = time.time() - start_time
            
            final_result = {
                "success": True,
                "customer_query": customer_query,
                "user_id": user_id,
                "timestamp": datetime.now().isoformat(),
                "processing_time": processing_time,
                "faq_response": faq_response,
                "escalation_decision": escalation_decision,
                "logging_result": logging_result,
                "final_status": "escalated_to_human" if escalation_decision["escalate"] else "resolved_by_bot",
                "recommended_action": self._get_recommended_action(escalation_decision, faq_response)
            }
            
            print(f"\n✅ Query processed successfully in {processing_time:.2f} seconds")
            self._print_summary(final_result)
            
            return final_result
            
        except Exception as e:
            error_result = {
                "success": False,
                "error": str(e),
                "customer_query": customer_query,
                "user_id": user_id,
                "timestamp": datetime.now().isoformat(),
                "processing_time": time.time() - start_time
            }
            
            print(f"❌ Error processing query: {e}")
            return error_result
    
    def _get_recommended_action(self, escalation_decision: Dict[str, Any], faq_response: Dict[str, Any]) -> str:
        """Get recommended next action based on the analysis"""
        if escalation_decision.get("escalate", False):
            agent_type = escalation_decision.get("human_agent_suggestion", "general_support")
            priority = escalation_decision.get("priority", "normal")
            return f"Route to {agent_type} with {priority} priority"
        else:
            confidence = faq_response.get("confidence", 0.5)
            if confidence >= 0.8:
                return "Customer query resolved - no further action needed"
            else:
                return "Response provided - monitor for customer satisfaction"
    
    def _print_summary(self, result: Dict[str, Any]) -> None:
        """Print a formatted summary of the interaction results"""
        print("\n📊 INTERACTION SUMMARY")
        print("=" * 40)
        
        faq = result.get("faq_response", {})
        escalation = result.get("escalation_decision", {})
        
        print(f"Query: {result.get('customer_query', 'N/A')[:80]}...")
        print(f"FAQ Confidence: {faq.get('confidence', 'N/A')}")
        print(f"Category: {faq.get('category', 'N/A')}")
        print(f"Escalated: {'Yes' if escalation.get('escalate') else 'No'}")
        if escalation.get("escalate"):
            print(f"Escalation Reason: {escalation.get('reason', 'N/A')}")
            print(f"Priority: {escalation.get('priority', 'N/A')}")
        print(f"Processing Time: {result.get('processing_time', 0):.2f}s")
        print(f"Final Status: {result.get('final_status', 'N/A')}")
        print("=" * 40)

def create_customer_support_crew() -> CustomerSupportCrew:
    """Factory function to create a configured customer support crew"""
    return CustomerSupportCrew()