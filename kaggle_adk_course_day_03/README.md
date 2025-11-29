# Day 3: Agent Teams with Session Management

## Overview
This directory focuses on advanced agent architecture with teams, session management, and persistent memory. You'll learn about session management and stateful interactions, agent teams with specialized roles, context compaction and memory management, and persistent memory across sessions.

## Contents
- `my_agent_team`: Complete agent team with weather checking capabilities
- `my_agent`: General-purpose agent for the day
- Multiple memory strategies:
  - `agent with_context_compaction.py`: Agent using context compaction techniques
  - `agent with_persistent_memory.py`: Agent using persistent memory
  - `agent with_session_state_tools.py`: Agent using session state tools
  - `agent with_stateful_memory.py`: Agent using stateful memory

## Prerequisites
- Python 3.8 or higher
- A Google API key for Gemini models
- Git for version control

## Installation

### 1. Setup Virtual Environment
```bash
# Navigate to the day's directory
cd kaggle_adk_course_day_03

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
OPENAI_API_KEY=your_openai_api_key_here (optional)
ANTHROPIC_API_KEY=your_anthropic_api_key_here (optional)
```

## How to Run

### 1. Navigate to the Agent Directory
```bash
cd my_agent_team
```

### 2. Run the Agent
```bash
python agent.py
```

## Learning Objectives
- Understand how to create agent teams with specialized roles
- Learn about session management for maintaining state across interactions
- Implement persistent memory for agents
- Use context compaction techniques to manage long conversations
- Integrate multiple LLM providers in a single agent team

## Key Concepts
- **Session Service**: Manages state across multiple interactions with the same user
- **Persistent Memory**: Maintains information across multiple sessions
- **Context Compaction**: Techniques to manage memory in long-running conversations
- **Agent Teams**: Multiple specialized agents working together
- **Multi-Provider Support**: Integration with different LLM providers (Google, OpenAI, Anthropic)

## Example Use Cases
- **Weather Agent**: A specialized agent that can provide weather information for specific cities
- **Conversational Memory**: Maintains context during extended conversations with users
- **Multi-Provider Integration**: Uses different LLMs for different tasks based on their strengths

## Memory Strategies
- **Context Compaction**: Reduces memory usage by summarizing past interactions
- **Persistent Memory**: Maintains important information across different sessions
- **Session State Tools**: Tools that maintain state during a single session
- **Stateful Memory**: Continuously evolving memory that adapts to new information

## Next Steps
After completing this day, move on to Day 4 to learn about home automation agents with custom plugins.