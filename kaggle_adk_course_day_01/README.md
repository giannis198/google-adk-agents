# Day 1: Introduction to Basic and Multi-Agent Systems

## Overview
This directory contains the foundational concepts of creating agents using Google ADK. You'll learn about basic agent creation, simple instruction-based agents, and multi-agent systems.

## Contents
- `my_agent`: A simple, helpful assistant agent
- `my_multi_agent`: Introduction to multiple agents working together
- `my_multi_loop_agent`: Loop-based multi-agent interactions
- `my_multi_parallel_agent`: Parallel execution of multiple agents
- `my_multi_sequential_agent`: Sequential execution of multiple agents

## Prerequisites
- Python 3.8 or higher
- A Google API key for Gemini models
- Git for version control

## Installation

### 1. Setup Virtual Environment
```bash
# Navigate to the day's directory
cd kaggle_adk_course_day_01

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
pip install google-adk python-dotenv
```

### 3. Set up Environment Variables
Create a `.env` file in the agent directories with your API keys:
```
GOOGLE_API_KEY=your_google_api_key_here
```

## How to Run

For each agent directory (my_agent, my_multi_agent, etc.), you can run the agent as follows:

### 1. Navigate to the Agent Directory
```bash
cd my_agent
```

### 2. Run the Agent
```bash
python agent.py
```

## Learning Objectives
- Understand the basic structure of an ADK agent
- Learn how to define a simple agent with the Gemini model
- Explore how to add tools to your agent (e.g., Google Search)
- Experience different multi-agent configurations (parallel, sequential, loop-based)

## Key Concepts
- **Agent**: The core component that processes user input and generates responses
- **Runner**: Manages the agent's execution environment
- **Model**: The LLM that powers the agent (in this case, Gemini)
- **Tools**: External functions that extend the agent's capabilities

## Next Steps
After completing this day, move on to Day 2 to learn about advanced agents with tools and human interaction.