import os
import json
import datetime
from crewai import Agent
from crewai_tools import BaseTool
from typing import Dict, Any

class LoggingTool(BaseTool):
    name: str = "Customer Interaction Logger"
    description: str = "Logs all customer interactions, responses, and escalation decisions to tracking system"
    
    def _run(self, interaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Log customer interaction data to file or database simulation
        """
        try:
            # Generate unique interaction ID
            timestamp = datetime.datetime.now()
            interaction_id = f"CS_{timestamp.strftime('%Y%m%d_%H%M%S')}_{hash(str(interaction_data)) % 10000:04d}"
            
            # Structure the log entry
            log_entry = {
                "interaction_id": interaction_id,
                "timestamp": timestamp.isoformat(),
                "customer_query": interaction_data.get("customer_query", ""),
                "faq_response": interaction_data.get("faq_response", {}),
                "escalation_decision": interaction_data.get("escalation_decision", {}),
                "user_id": interaction_data.get("user_id", "anonymous"),
                "session_id": interaction_data.get("session_id", ""),
                "channel": interaction_data.get("channel", "web"),
                "resolution_status": self._determine_resolution_status(interaction_data),
                "metadata": {
                    "mock_mode": os.getenv("MOCK_MODE", "true"),
                    "processing_time": interaction_data.get("processing_time", 0),
                    "agent_versions": {
                        "faq_agent": "1.0.0",
                        "escalation_agent": "1.0.0",
                        "logging_agent": "1.0.0"
                    }
                }
            }
            
            # Log to file (simulating database)
            self._write_to_log_file(log_entry)
            
            # Log to console for immediate visibility
            self._log_to_console(log_entry)
            
            # Generate analytics summary
            analytics = self._generate_analytics(log_entry)
            
            return {
                "logged": True,
                "interaction_id": interaction_id,
                "timestamp": timestamp.isoformat(),
                "analytics": analytics,
                "log_location": "logs/customer_interactions.json"
            }
            
        except Exception as e:
            error_log = {
                "logged": False,
                "error": str(e),
                "timestamp": datetime.datetime.now().isoformat(),
                "fallback_data": interaction_data
            }
            print(f"Logging Error: {error_log}")
            return error_log
    
    def _write_to_log_file(self, log_entry: Dict[str, Any]) -> None:
        """
        Write log entry to JSON file (simulating database storage)
        """
        # Ensure logs directory exists
        os.makedirs("logs", exist_ok=True)
        
        log_file_path = "logs/customer_interactions.json"
        
        # Read existing logs or create new list
        try:
            if os.path.exists(log_file_path):
                with open(log_file_path, "r") as file:
                    logs = json.load(file)
            else:
                logs = []
        except (json.JSONDecodeError, FileNotFoundError):
            logs = []
        
        # Append new log entry
        logs.append(log_entry)
        
        # Keep only last 1000 entries to prevent file from growing too large
        if len(logs) > 1000:
            logs = logs[-1000:]
        
        # Write back to file
        with open(log_file_path, "w") as file:
            json.dump(logs, file, indent=2, default=str)
    
    def _log_to_console(self, log_entry: Dict[str, Any]) -> None:
        """
        Print formatted log entry to console
        """
        escalated = log_entry.get("escalation_decision", {}).get("escalate", False)
        status_icon = "🚨" if escalated else "✅"
        
        print(f"\n{status_icon} CUSTOMER INTERACTION LOGGED")
        print(f"ID: {log_entry['interaction_id']}")
        print(f"Time: {log_entry['timestamp']}")
        print(f"Query: {log_entry['customer_query'][:100]}...")
        print(f"Resolution: {log_entry['resolution_status']}")
        if escalated:
            escalation = log_entry['escalation_decision']
            print(f"Escalation: {escalation.get('reason', 'N/A')} (Priority: {escalation.get('priority', 'N/A')})")
        print("-" * 50)
    
    def _determine_resolution_status(self, interaction_data: Dict[str, Any]) -> str:
        """
        Determine the resolution status based on interaction data
        """
        escalation_decision = interaction_data.get("escalation_decision", {})
        
        if escalation_decision.get("escalate", False):
            priority = escalation_decision.get("priority", "normal")
            return f"escalated_{priority}"
        else:
            faq_response = interaction_data.get("faq_response", {})
            confidence = faq_response.get("confidence", 0.5)
            
            if confidence >= 0.8:
                return "resolved_high_confidence"
            elif confidence >= 0.6:
                return "resolved_medium_confidence"
            else:
                return "resolved_low_confidence"
    
    def _generate_analytics(self, log_entry: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate basic analytics for this interaction
        """
        escalation_decision = log_entry.get("escalation_decision", {})
        faq_response = log_entry.get("faq_response", {})
        
        return {
            "escalated": escalation_decision.get("escalate", False),
            "confidence_score": faq_response.get("confidence", 0.0),
            "category": faq_response.get("category", "unknown"),
            "query_length": len(log_entry.get("customer_query", "")),
            "response_time": log_entry.get("metadata", {}).get("processing_time", 0),
            "suggested_agent": escalation_decision.get("human_agent_suggestion", "none")
        }

def create_logging_agent() -> Agent:
    """
    Create and configure the Logging Agent
    """
    return Agent(
        role="Customer Interaction Data Analyst",
        goal="Accurately log and track all customer service interactions for analysis and improvement",
        backstory="""You are a meticulous data analyst specializing in customer service operations. 
        You understand the importance of comprehensive logging for improving service quality, 
        identifying trends, and ensuring compliance with customer service standards. Your detailed 
        records help the organization learn and improve.""",
        tools=[LoggingTool()],
        verbose=True,
        allow_delegation=False
    )
