# Customer Support Agent Crew

A CrewAI-compatible automated customer support system that handles FAQ responses, escalation decisions, and interaction logging. This project follows the CrewAI Marketplace Template structure and is ready for submission to the [CrewAI Marketplace](https://marketplace.crewai.com).

## 🎯 Project Overview

The Customer Support Agent Crew is an intelligent automation system that processes customer queries through a coordinated team of AI agents:

- **FAQAgent**: Responds to frequently asked questions using a knowledge base or LLM
- **EscalationAgent**: Determines when to route queries to human agents based on confidence and complexity
- **LoggingAgent**: Records all interactions in a simulated ticketing system for analysis and tracking

## 🤖 Agent Roles

### FAQAgent
- Answers common customer questions about orders, shipping, returns, billing, and account issues
- Provides confidence scoring for responses
- Categorizes queries for better tracking
- Supports both mock responses and OpenAI API integration

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

## 🏗️ Project Structure

