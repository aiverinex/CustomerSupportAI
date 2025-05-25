#!/usr/bin/env python3
"""
Customer Support Agent Crew - Main Entry Point

A CrewAI-based customer support automation system that handles FAQ responses,
escalation decisions, and interaction logging.

Compatible with CrewAI Marketplace requirements.
"""

import os
import sys
import time
from datetime import datetime
from dotenv import load_dotenv

# Import CrewAI customer support crew
from crew.crew import create_customer_support_crew

def load_environment():
    """
    Load environment variables from .env file if it exists
    """
    if os.path.exists('.env'):
        load_dotenv()
        print("✅ Environment variables loaded from .env file")
    else:
        print("ℹ️  No .env file found, using system environment variables")
    
    # Display current configuration
    mock_mode = os.getenv("MOCK_MODE", "true").lower() == "true"
    has_openai_key = bool(os.getenv("OPENAI_API_KEY"))
    
    print(f"🔧 Configuration:")
    print(f"   Mock Mode: {'Enabled' if mock_mode else 'Disabled'}")
    print(f"   OpenAI API: {'Available' if has_openai_key else 'Not configured'}")
    if mock_mode:
        print("   ℹ️  Running in mock mode - no API calls will be made")

def load_sample_query():
    """
    Load sample query from file if available
    """
    sample_file = "sample_data/customer_query.txt"
    if os.path.exists(sample_file):
        try:
            with open(sample_file, 'r') as f:
                return f.read().strip()
        except Exception as e:
            print(f"⚠️  Could not read sample query: {e}")
    return None

def get_customer_input():
    """
    Get customer query from user input or use sample data
    """
    sample_query = load_sample_query()
    
    print("\n" + "="*60)
    print("🎯 CUSTOMER SUPPORT AGENT CREW")
    print("="*60)
    
    if sample_query:
        print(f"\n📄 Sample query available: {sample_query[:100]}...")
        use_sample = input("\nUse sample query? (y/n, default=y): ").strip().lower()
        if use_sample in ['', 'y', 'yes']:
            return sample_query, "sample_user_001"
    
    print("\n💬 Enter your customer support query:")
    print("   (or press Enter to use default query)")
    
    query = input("Query: ").strip()
    
    if not query:
        query = "Where is my order? I placed it 5 days ago and haven't received any tracking information."
        print(f"Using default query: {query}")
    
    user_id = input("User ID (optional, default=anonymous): ").strip() or "anonymous"
    
    return query, user_id

def run_interactive_mode():
    """
    Run the crew in interactive mode for testing
    """
    print("\n🚀 Starting Customer Support Agent Crew...")
    
    while True:
        try:
            # Get customer input
            customer_query, user_id = get_customer_input()
            
            if not customer_query:
                print("❌ No query provided. Exiting.")
                break
            
            # Process the query
            print(f"\n🔄 Processing query for user: {user_id}")
            crew = create_customer_support_crew()
            result = crew.process_customer_query(customer_query, user_id)
            
            # Display results
            if result.get("success"):
                print("\n✅ Query processed successfully!")
                
                # Show FAQ response
                faq = result.get("faq_response", {})
                if isinstance(faq, dict) and "answer" in faq:
                    print(f"\n💡 FAQ Response: {faq['answer']}")
                    print(f"   Confidence: {faq.get('confidence', 'N/A')}")
                    print(f"   Category: {faq.get('category', 'N/A')}")
                
                # Show escalation decision
                escalation = result.get("escalation_decision", {})
                if escalation.get("escalate"):
                    print(f"\n🚨 Escalation Required:")
                    print(f"   Reason: {escalation.get('reason', 'N/A')}")
                    print(f"   Priority: {escalation.get('priority', 'N/A')}")
                    print(f"   Suggested Agent: {escalation.get('human_agent_suggestion', 'N/A')}")
                else:
                    print("\n✅ Query resolved by automated system")
                
                # Show final recommendation
                print(f"\n📋 Recommended Action: {result.get('recommended_action', 'N/A')}")
                
            else:
                print(f"\n❌ Error processing query: {result.get('error', 'Unknown error')}")
            
            # Ask if user wants to continue
            print("\n" + "-"*60)
            continue_choice = input("Process another query? (y/n, default=n): ").strip().lower()
            if continue_choice not in ['y', 'yes']:
                break
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Thanks for using Customer Support Agent Crew.")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            continue

def run_batch_mode(queries_file: str):
    """
    Run the crew in batch mode processing multiple queries from a file
    """
    if not os.path.exists(queries_file):
        print(f"❌ Queries file not found: {queries_file}")
        return
    
    print(f"\n📁 Running batch processing from: {queries_file}")
    crew = create_customer_support_crew()
    
    try:
        with open(queries_file, 'r') as f:
            queries = [line.strip() for line in f if line.strip()]
        
        results = []
        for i, query in enumerate(queries, 1):
            print(f"\n🔄 Processing query {i}/{len(queries)}: {query[:50]}...")
            result = crew.process_customer_query(query, f"batch_user_{i:03d}")
            results.append(result)
        
        # Generate batch summary
        print(f"\n📊 BATCH PROCESSING SUMMARY")
        print("="*40)
        total_queries = len(results)
        successful = sum(1 for r in results if r.get("success"))
        escalated = sum(1 for r in results if r.get("escalation_decision", {}).get("escalate"))
        
        print(f"Total Queries: {total_queries}")
        print(f"Successful: {successful}")
        print(f"Failed: {total_queries - successful}")
        print(f"Escalated: {escalated}")
        print(f"Resolution Rate: {(successful - escalated) / total_queries * 100:.1f}%")
        print("="*40)
        
    except Exception as e:
        print(f"❌ Error in batch processing: {e}")

def main():
    """
    Main entry point for the Customer Support Agent Crew
    """
    print("🎯 Customer Support Agent Crew v1.0.0")
    print("   CrewAI Marketplace Compatible")
    print("   https://marketplace.crewai.com")
    
    # Load environment configuration
    load_environment()
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--batch" and len(sys.argv) > 2:
            run_batch_mode(sys.argv[2])
        elif sys.argv[1] == "--help":
            print("\nUsage:")
            print("  python main.py                    # Interactive mode")
            print("  python main.py --batch <file>     # Batch process queries from file")
            print("  python main.py --help             # Show this help")
        else:
            print(f"❌ Unknown argument: {sys.argv[1]}")
            print("Use --help for usage information")
    else:
        # Run in interactive mode
        run_interactive_mode()

if __name__ == "__main__":
    main()
