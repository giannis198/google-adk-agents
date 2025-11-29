# Day 2: Advanced Agents with Tools and Human Interaction

## Overview
This directory builds upon the basic concepts from Day 1 and introduces more sophisticated agents with external tools and human interaction. You'll learn about calculation agents with code execution capabilities, human-in-the-loop agents, and image generation with approval workflows.

## Contents
- `my_calculation_agent`: Specialized calculator agent with code execution capabilities
- `my_HumanInLoop_agent`: Agent requiring human approval for certain operations
- `my_image_generation_with_approval_agent`: Image generation with approval workflow
- `my_mcp_agent`: Agent using Model Context Protocol
- `my_agent`: Enhanced general-purpose agent with various tools

## Prerequisites
- Python 3.8 or higher
- A Google API key for Gemini models
- Git for version control

## Installation

### 1. Setup Virtual Environment
```bash
# Navigate to the day's directory
cd kaggle_adk_course_day_02

# Create a virtual environment
python -m venv myenv

# Activate the virtual environment
# On Linux/Mac:
source myenv/bin/activate
# On Windows:
myenv\Scripts\activate
```

### 2. Install Dependencies
```bash
# Install Google ADK and other required packages
pip install google-adk python-dotenv uvicorn fastapi
```

### 3. Set up Environment Variables
Create a `.env` file in the agent directories with your API keys:
```
GOOGLE_API_KEY=your_google_api_key_here
```

## How to Run

For each agent directory (my_calculation_agent, my_HumanInLoop_agent, etc.), you can run the agent as follows:

### 1. Navigate to the Agent Directory
```bash
cd my_calculation_agent
```

### 2. Run the Agent
```bash
python agent.py
```

## Learning Objectives
- Understand how to create agents with specialized calculation capabilities
- Learn how to implement human-in-the-loop functionality
- Explore image generation with approval workflows
- Implement custom function tools for agents
- Understand how to use other agents as tools

## Key Concepts
- **Code Executor**: Allows agents to execute Python code securely
- **Custom Function Tools**: Extend agent capabilities with domain-specific functions
- **Agent Tools**: Use other agents as tools within an agent
- **Retry Configuration**: Handle API failures gracefully
- **Human-in-the-Loop**: Integrate human approval in agent workflows

## Example Use Cases
- **Calculation Agent**: Performs complex calculations by generating and executing Python code
- **Currency Conversion Agent**: Combines multiple tools to provide accurate currency conversions with fees
- **Human Approval Agent**: Ensures sensitive operations are approved by a human before execution

## Next Steps
After completing this day, move on to Day 3 to learn about agent teams with session management and persistent memory.