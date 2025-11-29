# Kaggle ADK (Agent Development Kit) Course

Welcome to the Kaggle ADK Course! This repository contains a comprehensive learning path for developing agents using Google's Agent Development Kit. Each day of the course builds upon previous concepts, introducing new features and capabilities of the ADK framework.

## Overview

The course is structured as a 5-day journey through different aspects of agent development:
- **Day 1**: Introduction to basic agents and multi-agent systems
- **Day 2**: Advanced agents with tools, calculations, and human-in-the-loop
- **Day 3**: Agent teams with session management and persistent memory
- **Day 4**: Home automation agents with custom plugins
- **Day 5**: Agent-to-Agent (A2A) communication protocols

## Prerequisites

Before starting the course, ensure you have:
- Python 3.8 or higher
- A Google API key for Gemini models
- Git for version control

## Setup

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd kaggle_adk_course
   ```

2. For each day's exercises, navigate to the respective directory and create a virtual environment:
   ```bash
   cd kaggle_adk_course_day_0X  # Replace X with the day number
   python -m venv myenv
   source myenv/bin/activate  # On Windows: myenv\Scripts\activate
   pip install -r ../kaggle_adk_course_day_05/requirements.txt  # or install manually: pip install google-adk python-dotenv
   ```

3. Create a `.env` file in each agent directory with your API keys:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```

## Course Structure

### Day 1: Introduction to Basic and Multi-Agent Systems
**Directory**: `kaggle_adk_course_day_01`

This day introduces the fundamental concepts of creating agents using Google ADK. You'll learn about:
- Basic agent creation with the Gemini model
- Simple instruction-based agents
- Multi-agent systems (parallel, sequential, loop-based)
- In-memory runners for local execution

**Agent Types**:
- `my_agent`: A simple, helpful assistant agent
- `my_multi_agent`: Introduction to multiple agents working together
- `my_multi_loop_agent`: Loop-based multi-agent interactions
- `my_multi_parallel_agent`: Parallel execution of multiple agents
- `my_multi_sequential_agent`: Sequential execution of multiple agents

### Day 2: Advanced Agents with Tools and Human Interaction
**Directory**: `kaggle_adk_course_day_02`

Building upon day 1, this day introduces more sophisticated agents with external tools and human interaction:
- Calculation agents with code execution capabilities
- Human-in-the-loop agents with approval processes
- Image generation with approval workflows
- MCP (Model Context Protocol) agents
- Tool integration (Google Search, custom functions, other agents)

**Agent Types**:
- `my_calculation_agent`: Specialized calculator agent with code execution
- `my_HumanInLoop_agent`: Agent requiring human approval for certain operations
- `my_image_generation_with_approval_agent`: Image generation with approval workflow
- `my_mcp_agent`: Agent using Model Context Protocol
- `my_agent`: Enhanced general-purpose agent

### Day 3: Agent Teams with Session Management
**Directory**: `kaggle_adk_course_day_03`

This day focuses on advanced agent architecture with teams, session management, and persistent memory:
- Session management and stateful interactions
- Agent teams with specialized roles
- Context compaction and memory management
- Persistent memory across sessions
- Integration with multiple LLM providers

**Features**:
- `my_agent_team`: Complete agent team with weather checking capabilities
- Multiple memory strategies (with_context_compaction, with_persistent_memory, with_session_state_tools, with_stateful_memory)
- Multi-provider support (Google, OpenAI, Anthropic)

### Day 4: Home Automation with Custom Plugins
**Directory**: `kaggle_adk_course_day_04`

This day demonstrates real-world applications by creating home automation agents with custom plugins:
- Plugin development for monitoring and extending agent capabilities
- Home automation scenarios
- Custom agent creation patterns
- Invocation counting and monitoring plugins

**Components**:
- `home_automation_agent`: Smart home control agent
- `my-agent`: Additional agent implementation
- `plugin.py`: Custom plugin system for tracking agent and tool invocations
- `logs.py`: Logging utilities
- `logger.log`: Example log file

### Day 5: Agent-to-Agent (A2A) Communication
**Directory**: `kaggle_adk_course_day_05`

The final day explores distributed agent systems with inter-agent communication:
- Agent-to-Agent (A2A) protocol implementation
- Remote agent communication
- Tool sharing between agents
- Service discovery using agent cards
- Distributed agent architectures

**Components**:
- `my_a2a_agent`: Product catalog agent and customer support agent with A2A communication
- A2A protocol implementation
- Remote agent proxy system
- Product catalog with mock data

## Technology Stack

- **Google ADK (Agent Development Kit)**: Core framework for creating agents
- **Gemini Models**: Primary LLM integration (2.5-flash-lite, 2.0-flash)
- **Python 3.8+**: Core programming language
- **Virtual Environments**: For dependency isolation
- **Environment Variables**: For API key management
- **Various Tools**: Google Search, Code Executors, Custom Functions

## Getting Started

1. Start with Day 1 to understand the basics
2. Progress through each day sequentially
3. Experiment with the provided examples
4. Modify the agents to understand how different components work
5. Refer to the documentation in each day's directory for specific instructions

## Important Notes

- Each day's directory contains its own virtual environment (`myenv`)
- API keys are stored in `.env` files and should not be committed to version control
- The `.gitignore` file has been configured to exclude sensitive and temporary files
- Some directories may contain multiple agent implementations to demonstrate different approaches

## Learning Outcomes

By completing this course, you will have:
- Understanding of Google ADK and its components
- Experience creating single and multi-agent systems
- Knowledge of tool integration and custom function creation
- Experience with session management and persistent memory
- Understanding of plugin architecture
- Knowledge of distributed agent systems and A2A communication
- Practical experience with real-world agent implementations

## Contributing

This repository contains educational material from the Kaggle ADK course. If you find issues or have suggestions for improvements, feel free to create an issue or submit a pull request.

## License

[Specify license here if applicable]