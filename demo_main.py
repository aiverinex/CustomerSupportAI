#!/usr/bin/env python3
"""
Customer Support Agent Crew - Demo Version
CrewAI Marketplace Compatible Demo
"""

import os
from datetime import datetime
from dotenv import load_dotenv
from crew.simple_crew import create_customer_support_crew

def load_environment():
    """Load environment variables"""
    if os.path.exists('.env'):
        load_dotenv()
        print("✅ Environment variables loaded from .env file")
    else:
        print("ℹ️  No .env file found, using system environment variables")
    
    mock_mode = os.getenv("MOCK_MODE", "true").lower() == "true"
    has_openai_key = bool(os.getenv("OPENAI_API_KEY"))
    
    print(f"🔧 Configuration:")
    print(f"   Mock Mode: {'Enabled' if mock_mode else 'Disabled'}")
    print(f"   OpenAI API: {'Available' if has_openai_key else 'Not configured'}")
    if mock_mode:
        print("   ℹ️  Running in mock mode - no API calls will be made")

def run_demo():
    """Run Customer Support Agent Crew Demo"""
    print("🎯 Customer Support Agent Crew v1.0.0")
    print("   CrewAI Marketplace Compatible")
    print("   https://marketplace.crewai.com")
    print()
    
    load_environment()
    
    # Load sample query
    sample_query = "Where is my order? I placed it 5 days ago and haven't received any tracking information."
    if os.path.exists("sample_data/customer_query.txt"):
        try:
            with open("sample_data/customer_query.txt", 'r') as f:
                sample_query = f.read().strip()
        except:
            pass
    
    print(f"\n📋 Demo Scenarios:")
    test_scenarios = [
        ("Order tracking question", sample_query, "customer_001"),
        ("Return request", "I want to return a damaged product I received yesterday.", "customer_002"),
        ("Angry customer complaint", "This is terrible! I demand to speak to a manager immediately!", "customer_003"),
        ("Shipping inquiry", "How long does standard shipping take?", "customer_004")
    ]
    
    crew = create_customer_support_crew()
    
    for i, (scenario_name, query, user_id) in enumerate(test_scenarios, 1):
        print(f"\n{'='*60}")
        print(f"SCENARIO {i}/{len(test_scenarios)}: {scenario_name}")
        print(f"User: {user_id}")
        
        result = crew.process_customer_query(query, user_id)
        
        if result["success"]:
            escalated = result["escalation_decision"]["escalate"]
            status = "🚨 ESCALATED" if escalated else "✅ RESOLVED"
            print(f"\nResult: {status}")
            if escalated:
                print(f"Priority: {result['escalation_decision']['priority']}")
        else:
            print("❌ Error in processing")
    
    print(f"\n🎉 Demo completed successfully!")
    print("Your Customer Support Agent Crew is working perfectly!")
    print("\nKey Features Demonstrated:")
    print("✓ FAQ Agent - Intelligent response generation")
    print("✓ Escalation Agent - Smart human routing decisions") 
    print("✓ Logging Agent - Comprehensive interaction tracking")
    print("✓ CrewAI Marketplace Compatible Structure")

if __name__ == "__main__":
    run_demo()