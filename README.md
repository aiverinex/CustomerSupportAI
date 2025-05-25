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

```
customer-support-crew/
├── agents/
│   ├── faq_agent.py          # FAQ response agent
│   ├── escalation_agent.py   # Escalation decision agent
│   └── logging_agent.py      # Interaction logging agent
├── tasks/
│   └── task.py              # Task definitions for the workflow
├── crew/
│   └── crew.py              # Main crew orchestration
├── config/
│   └── config.yaml          # Configuration settings
├── sample_data/
│   └── customer_query.txt   # Sample customer queries for testing
├── main.py                  # Main entry point
├── README.md               # Project documentation
└── pyproject.toml          # Project dependencies
```

## 🔧 Features

- **AI-Powered Responses**: Uses OpenAI's advanced language models for intelligent customer support
- **Automatic Escalation**: Smart detection of when human intervention is needed
- **Comprehensive Logging**: Detailed interaction tracking with analytics
- **CrewAI Compatible**: Built following CrewAI Marketplace standards
- **Production Ready**: Scalable architecture for real customer support workflows

## 📊 Agent Workflow

1. **Customer Query Input** → FAQ Agent analyzes and responds
2. **FAQ Response** → Escalation Agent evaluates need for human support
3. **Complete Interaction** → Logging Agent records everything for analysis

## 🤝 Contributing

This project follows the CrewAI Marketplace Template structure. For contributions or marketplace submission, ensure all agents maintain the established interfaces and follow CrewAI best practices.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
