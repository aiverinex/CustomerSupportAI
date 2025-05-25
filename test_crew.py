#!/usr/bin/env python3
"""
Test script for Customer Support Agent Crew
"""

import os
from crew.crew import create_customer_support_crew

def test_customer_support_crew():
    """Test the customer support crew with a sample query"""
    
    print("🎯 Testing Customer Support Agent Crew")
    print("=" * 50)
    
    # Create the crew
    crew = create_customer_support_crew()
    
    # Test query
    test_query = "Where is my order? I placed it 5 days ago and haven't received any tracking information. The order number is #12345."
    
    print(f"📞 Customer Query: {test_query}")
    print("\n🤖 Processing with AI agents...")
    print("-" * 50)
    
    # Process the query
    result = crew.process_customer_query(
        customer_query=test_query,
        user_id="test_user_123",
        session_id="test_session_456"
    )
    
    print("\n✅ Processing Complete!")
    print("=" * 50)
    
    return result

if __name__ == "__main__":
    try:
        result = test_customer_support_crew()
        print(f"\n🎉 Test completed successfully!")
        print(f"📊 Final Status: {result.get('final_status', 'Unknown')}")
        print(f"⏱️ Processing Time: {result.get('processing_time', 0):.2f} seconds")
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")