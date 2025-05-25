# Customer Support Agent Crew

A CrewAI-compatible automated customer support system that handles FAQ responses, escalation decisions, and interaction logging. This project follows the CrewAI Marketplace Template structure and is ready for submission to the [CrewAI Marketplace](https://marketplace.crewai.com).

## 🎯 Project Overview

The Customer Support Agent Crew is an intelligent automation system that processes customer queries through a coordinated team of AI agents:

- **FAQAgent**: Responds to frequently asked questions using OpenAI's advanced language models
- **EscalationAgent**: Determines when to route queries to human agents based on confidence and complexity
- **LoggingAgent**: Records all interactions in a simulated ticketing system for analysis and tracking

## 🤖 Agent Roles

### FAQAgent
- Answers common customer questions about orders, shipping, returns, billing, and account issues
- Provides intelligent, contextual responses using OpenAI's advanced language models
- Includes confidence scoring for response quality assessment
- Categorizes queries automatically for better tracking and analytics

### EscalationAgent  
- Analyzes FAQ responses and customer queries for escalation needs
- Evaluates confidence levels, emotional tone, and complexity
- Sets priority levels (low, normal, high, urgent)
- Suggests appropriate human agent types (general, technical, billing, manager)

### LoggingAgent
- Creates comprehensive interaction logs with unique IDs
- Tracks resolution status and analytics
- Simulates database storage via JSON files
- Generates performance metrics and summaries

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- OpenAI API key

### Setup
1. Clone or download this project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your OpenAI API key as an environment variable:
   ```bash
   export OPENAI_API_KEY=your_api_key_here
   ```
4. Run the Customer Support Agent Crew:
   ```bash
   python main.py
   ```

### Usage
The system will prompt you to use a sample query or enter your own customer support question. The three AI agents will work together to:
1. Provide an intelligent FAQ response
2. Determine if escalation to human support is needed
3. Log the complete interaction for analysis

## 🏗️ Project Structure

