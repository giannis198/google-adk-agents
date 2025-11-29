# Day 4: Home Automation with Custom Plugins

## Overview
This directory demonstrates real-world applications by creating home automation agents with custom plugins. You'll learn about plugin development for monitoring and extending agent capabilities, home automation scenarios, custom agent creation patterns, and invocation counting and monitoring plugins.

## Contents
- `home_automation_agent`: Smart home control agent
- `my-agent`: Additional agent implementation for home automation
- `plugin.py`: Custom plugin system for tracking agent and tool invocations
- `logs.py`: Logging utilities
- `logger.log`: Example log file

## Prerequisites
- Python 3.8 or higher
- A Google API key for Gemini models
- Git for version control

## Installation

### 1. Setup Virtual Environment
```bash
# Navigate to the day's directory
cd kaggle_adk_course_day_04

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

### 1. Navigate to the Agent Directory
```bash
cd home_automation_agent
```

### 2. Run the Agent
```bash
python agent.py
```

## Learning Objectives
- Understand how to develop custom plugins for agents
- Learn how to monitor agent and tool invocations
- Implement real-world home automation scenarios
- Create custom agent behaviors using plugins
- Track and log agent activities for debugging and analytics

## Key Concepts
- **Plugins**: Extend agent functionality with custom logic
- **Callbacks**: Execute custom code at specific points in the agent lifecycle
- **Monitoring**: Track agent and tool usage for analytics
- **Home Automation**: Real-world application of agent technology
- **Invocation Counting**: Track how often agents and tools are used

## Plugin Architecture
The custom plugin system in `plugin.py` demonstrates:
- `before_agent_callback`: Runs before an agent is called
- `before_model_callback`: Runs before a model is called
- Custom counters for tracking agent and tool usage
- Logging of invocation data

## Example Use Cases
- **Smart Home Control**: Control lighting, temperature, and other home systems
- **Device Monitoring**: Track and respond to home device status changes
- **Energy Management**: Optimize home energy consumption
- **Security Systems**: Monitor and control home security features

## Architecture
```
Home Automation Agent
    ↓
Custom Plugin System
    ↓
Device Control Logic
    ↓
Smart Home Devices
```

## Next Steps
After completing this day, move on to Day 5 to learn about Agent-to-Agent (A2A) communication for distributed agent systems.