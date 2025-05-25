#!/usr/bin/env python3
"""
Demo test for Customer Support Agent Crew in mock mode
"""

import os
import sys
from crew.crew import create_customer_support_crew

def demo_customer_support():
    """Demonstrate the customer support crew with sample queries"""
    
    print("🎯 Customer Support Agent Crew Demo")
    print("Running in Mock Mode - No API keys required")
    print("=" * 60)
    
    # Test queries
    test_queries = [
        "Where is my order? I placed it 5 days ago and haven't received any tracking information. Order #12345.",
        "I want to return this item. It doesn't fit properly.",
        "URGENT: I was charged twice for the same order! This is unacceptable!"
    ]
    
    # Create the crew
    print("🤖 Initializing Customer Support Crew...")
    crew = create_customer_support_crew()
    print("✅ Crew initialized with 3 agents: FAQ, Escalation, and Logging")
    print()
    
    for i, query in enumerate(test_queries, 1):
        print(f"📞 Test {i}: {query}")
        print("-" * 60)
        
        try:
            # Process the query
            result = crew.process_customer_query(
                customer_query=query,
                user_id=f"demo_user_{i}",
                session_id=f"demo_session_{i}"
            )
            
            print("✅ Processing completed successfully!")
            print(f"📊 Status: {result.get('final_status', 'completed')}")
            print(f"⏱️ Time: {result.get('processing_time', 0):.2f}s")
            print()
            
        except Exception as e:
            print(f"❌ Error processing query: {str(e)}")
            print()
    
    print("🎉 Demo completed! All three agents working together:")
    print("  📋 FAQ Agent - Provides helpful responses to customer questions")
    print("  🚨 Escalation Agent - Decides when human intervention is needed")
    print("  📝 Logging Agent - Records all interactions for analysis")

if __name__ == "__main__":
    demo_customer_support()