import time
import json
from datetime import datetime
from crewai import Crew, Process
from agents.faq_agent import create_faq_agent
from agents.escalation_agent import create_escalation_agent
from agents.logging_agent import create_logging_agent
from tasks.task import create_faq_task, create_escalation_task, create_logging_task
from typing import Dict, Any, Optional

class CustomerSupportCrew:
    """
    CrewAI-based customer support automation system
    """
    
    def __init__(self):
        """
        Initialize the customer support crew with all agents
        """
        self.faq_agent = create_faq_agent()
        self.escalation_agent = create_escalation_agent()
        self.logging_agent = create_logging_agent()
        
        self.crew = Crew(
            agents=[self.faq_agent, self.escalation_agent, self.logging_agent],
            process=Process.sequential,
            verbose=True
        )
    
    def process_customer_query(self, customer_query: str, user_id: str = "anonymous", session_id: str = "") -> Dict[str, Any]:
        """
        Process a customer query through the complete support workflow
        
        Args:
            customer_query: The customer's question or concern
            user_id: Unique identifier for the customer (default: "anonymous")
            session_id: Session identifier for tracking (default: "")
        
        Returns:
            Complete interaction result with all agent responses
        """
        start_time = time.time()
        
        try:
            print(f"\n🎯 Processing Customer Query: {customer_query}")
            print(f"👤 User ID: {user_id}")
            print(f"📅 Timestamp: {datetime.now().isoformat()}")
            print("=" * 60)
            
            # Create the workflow tasks
            faq_task = create_faq_task(self.faq_agent, customer_query)
            escalation_task = create_escalation_task(self.escalation_agent, "{faq_response}", customer_query)
            logging_task = create_logging_task(self.logging_agent, customer_query, "{faq_response}", "{escalation_decision}")
            
            # Set task dependencies
            escalation_task.context = [faq_task]
            logging_task.context = [faq_task, escalation_task]
            
            tasks = [faq_task, escalation_task, logging_task]
            
            # Execute the crew workflow
            self.crew.tasks = tasks
            results = self.crew.kickoff()
            
            processing_time = time.time() - start_time
            
            # Parse and structure the results
            final_result = self._structure_results(
                results, customer_query, user_id, session_id, processing_time
            )
            
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
    
    def _structure_results(self, results, customer_query: str, user_id: str, session_id: str, processing_time: float) -> Dict[str, Any]:
        """
        Structure the crew results into a comprehensive response
        """
        try:
            # Extract results from each task
            task_results = []
            if hasattr(results, 'tasks_output'):
                task_results = [task.raw for task in results.tasks_output]
            elif isinstance(results, list):
                task_results = results
            else:
                task_results = [str(results)]
            
            # Parse individual agent outputs
            faq_response = self._parse_agent_output(task_results[0] if len(task_results) > 0 else "")
            escalation_decision = self._parse_agent_output(task_results[1] if len(task_results) > 1 else "")
            logging_result = self._parse_agent_output(task_results[2] if len(task_results) > 2 else "")
            
            return {
                "success": True,
                "customer_query": customer_query,
                "user_id": user_id,
                "session_id": session_id,
                "timestamp": datetime.now().isoformat(),
                "processing_time": processing_time,
                "faq_response": faq_response,
                "escalation_decision": escalation_decision,
                "logging_result": logging_result,
                "final_status": self._determine_final_status(escalation_decision),
                "recommended_action": self._get_recommended_action(escalation_decision, faq_response)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to structure results: {str(e)}",
                "raw_results": str(results),
                "customer_query": customer_query,
                "user_id": user_id,
                "timestamp": datetime.now().isoformat(),
                "processing_time": processing_time
            }
    
    def _parse_agent_output(self, output: str) -> Dict[str, Any]:
        """
        Parse agent output, handling both JSON and plain text responses
        """
        if not output:
            return {"raw_output": "No output received"}
        
        try:
            # Try to parse as JSON first
            if isinstance(output, dict):
                return output
            elif isinstance(output, str):
                # Look for JSON in the output
                import re
                json_match = re.search(r'\{.*\}', output, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
                else:
                    return {"raw_output": output.strip()}
            else:
                return {"raw_output": str(output)}
        except (json.JSONDecodeError, AttributeError):
            return {"raw_output": str(output)}
    
    def _determine_final_status(self, escalation_decision: Dict[str, Any]) -> str:
        """
        Determine the final status of the customer interaction
        """
        if escalation_decision.get("escalate", False):
            priority = escalation_decision.get("priority", "normal")
            return f"escalated_to_human_{priority}"
        else:
            return "resolved_by_bot"
    
    def _get_recommended_action(self, escalation_decision: Dict[str, Any], faq_response: Dict[str, Any]) -> str:
        """
        Get recommended next action based on the analysis
        """
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
        """
        Print a formatted summary of the interaction results
        """
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
    """
    Factory function to create a configured customer support crew
    """
    return CustomerSupportCrew()
