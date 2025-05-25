import os
import json
from crewai import Agent
from openai import OpenAI
from typing import Dict, Any

def escalation_analysis(faq_response: str, customer_query: str) -> Dict[str, Any]:
    name: str = "Escalation Decision Engine"
    description: str = "Determines when customer queries should be escalated to human agents based on confidence and complexity"
    
    def _run(self, faq_response: str, customer_query: str) -> Dict[str, Any]:
        """
        Analyze FAQ response and determine if escalation is needed
        """
        mock_mode = os.getenv("MOCK_MODE", "true").lower() == "true"
        
        if mock_mode:
            return self._mock_escalation_decision(faq_response, customer_query)
        else:
            return self._openai_escalation_decision(faq_response, customer_query)
    
    def _mock_escalation_decision(self, faq_response: str, customer_query: str) -> Dict[str, Any]:
        """
        Mock escalation logic based on confidence thresholds and keywords
        """
        try:
            # Parse FAQ response if it's JSON
            if isinstance(faq_response, str):
                response_data = json.loads(faq_response)
            else:
                response_data = faq_response
            
            confidence = response_data.get("confidence", 0.5)
            category = response_data.get("category", "unknown")
            
            # Escalation criteria
            escalation_needed = False
            escalation_reason = ""
            priority = "normal"
            
            # Low confidence threshold
            if confidence < 0.6:
                escalation_needed = True
                escalation_reason = "Low confidence in automated response"
                priority = "high"
            
            # Complex query keywords that require human intervention
            complex_keywords = [
                "legal", "lawsuit", "attorney", "complaint", "damaged", "broken",
                "emergency", "urgent", "manager", "supervisor", "escalate",
                "unacceptable", "terrible", "worst", "hate", "fraud", "scam"
            ]
            
            query_lower = customer_query.lower()
            if any(keyword in query_lower for keyword in complex_keywords):
                escalation_needed = True
                escalation_reason = "Query contains keywords requiring human attention"
                priority = "urgent"
            
            # Category-based escalation
            if category in ["unknown", "error"]:
                escalation_needed = True
                escalation_reason = "Unable to categorize or process query"
            
            # Multiple question complexity
            if customer_query.count("?") > 2:
                escalation_needed = True
                escalation_reason = "Multiple complex questions require human review"
            
            return {
                "escalate": escalation_needed,
                "reason": escalation_reason,
                "priority": priority,
                "confidence_score": confidence,
                "category": category,
                "human_agent_suggestion": self._suggest_agent_type(category, customer_query)
            }
            
        except Exception as e:
            # Default to escalation if we can't parse the response
            return {
                "escalate": True,
                "reason": f"Error processing escalation decision: {str(e)}",
                "priority": "high",
                "confidence_score": 0.0,
                "category": "error",
                "human_agent_suggestion": "general_support"
            }
    
    def _openai_escalation_decision(self, faq_response: str, customer_query: str) -> Dict[str, Any]:
        """
        Use OpenAI to make sophisticated escalation decisions
        """
        try:
            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            # do not change this unless explicitly requested by the user
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            
            escalation_prompt = f"""
            You are an expert escalation manager for customer service. Analyze the following:
            
            Customer Query: {customer_query}
            FAQ Response: {faq_response}
            
            Determine if this should be escalated to a human agent based on:
            - Complexity of the query
            - Emotional tone or urgency
            - Whether the FAQ response adequately addresses the concern
            - Legal, billing, or technical complexity
            - Customer satisfaction indicators
            
            Respond in JSON format with:
            - escalate: boolean
            - reason: string explanation
            - priority: "low", "normal", "high", or "urgent"
            - confidence_score: float 0-1
            - category: string
            - human_agent_suggestion: "general_support", "technical", "billing", "manager"
            """
            
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an expert customer service escalation manager."},
                    {"role": "user", "content": escalation_prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            # Fallback to mock decision if API fails
            return self._mock_escalation_decision(faq_response, customer_query)
    
    def _suggest_agent_type(self, category: str, query: str) -> str:
        """
        Suggest the type of human agent needed
        """
        query_lower = query.lower()
        
        if category in ["billing", "payment"] or any(word in query_lower for word in ["bill", "charge", "payment", "refund"]):
            return "billing"
        elif category == "account" or any(word in query_lower for word in ["technical", "website", "app", "login", "bug"]):
            return "technical"
        elif any(word in query_lower for word in ["manager", "supervisor", "complaint", "legal"]):
            return "manager"
        else:
            return "general_support"

def create_escalation_agent() -> Agent:
    """
    Create and configure the Escalation Agent
    """
    return Agent(
        role="Escalation Decision Specialist",
        goal="Intelligently determine when customer queries require human intervention",
        backstory="""You are a seasoned customer service supervisor with years of experience 
        in managing complex customer situations. You have an excellent ability to assess 
        when automated responses are sufficient versus when human empathy, expertise, 
        or authority is needed to resolve customer concerns effectively.""",
        tools=[EscalationTool()],
        verbose=True,
        allow_delegation=False
    )
