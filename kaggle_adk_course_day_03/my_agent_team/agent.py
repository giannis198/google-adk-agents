# fixed_with_env.py
import os
import asyncio
from dotenv import load_dotenv
import warnings
warnings.filterwarnings("ignore")
import logging
logging.basicConfig(level=logging.ERROR)

# ADK imports (may raise ModuleNotFoundError if packages not installed)
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

# Load .env from current directory (or specify path: load_dotenv(".env"))
load_dotenv()

print("Libraries imported.")
google_key = os.getenv("GOOGLE_API_KEY")
openai_key = os.getenv("OPENAI_API_KEY")
anthropic_key = os.getenv("ANTHROPIC_API_KEY")

def key_is_set(k):
    return k is not None and k != "" and not k.startswith("YOUR_")

print("API Keys Set:")
print(f"Google API Key set: {'Yes' if key_is_set(google_key) else 'No'}")
print(f"OpenAI API Key set: {'Yes' if key_is_set(openai_key) else 'No'}")
print(f"Anthropic API Key set: {'Yes' if key_is_set(anthropic_key) else 'No'}")

os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"

# Model constants
MODEL_GEMINI_2_0_FLASH = "gemini-2.0-flash"
AGENT_MODEL = MODEL_GEMINI_2_0_FLASH

# Tool (mock)
def get_weather(city: str) -> dict:
    print(f"--- Tool: get_weather called for city: {city} ---")
    city_normalized = city.lower().replace(" ", "")
    mock_weather_db = {
        "newyork": {"status": "success", "report": "The weather in New York is sunny with a temperature of 25°C."},
        "london": {"status": "success", "report": "It's cloudy in London with a temperature of 15°C."},
        "tokyo": {"status": "success", "report": "Tokyo is experiencing light rain and a temperature of 18°C."},
    }
    return mock_weather_db.get(city_normalized, {"status": "error", "error_message": f"Sorry, I don't have weather information for '{city}'."})

print(get_weather("New York"))
print(get_weather("Paris"))

# Create agent
weather_agent = Agent(
    name="weather_agent_v1",
    model=AGENT_MODEL,
    description="Provides weather information for specific cities.",
    instruction=(
        "You are a helpful weather assistant. "
        "When the user asks for the weather in a specific city, "
        "use the 'get_weather' tool to find the information. "
        "If the tool returns an error, inform the user politely. "
        "If the tool is successful, present the weather report clearly."
    ),
    tools=[get_weather],
)
print(f"Agent '{weather_agent.name}' created using model '{AGENT_MODEL}'.")

# Session service and runner (runner uses session_service; session must still be created)
session_service = InMemorySessionService()

APP_NAME = "weather_tutorial_app"
USER_ID = "user_1"
SESSION_ID = "session_001"

# Create the runner (it's fine to create before the session, but session must exist before run_async)
runner = Runner(
    agent=weather_agent,
    app_name=APP_NAME,
    session_service=session_service
)
print(f"Runner created for agent '{runner.agent.name}'.")

# Agent interaction function
async def call_agent_async(query: str, runner, user_id, session_id):
    print(f"\n>>> User Query: {query}")
    content = types.Content(role='user', parts=[types.Part(text=query)])
    final_response_text = "Agent did not produce a final response."

    async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
            elif getattr(event, "actions", None) and getattr(event.actions, "escalate", False):
                final_response_text = f"Agent escalated: {getattr(event, 'error_message', 'No specific message.')}"
            break

    print(f"<<< Agent Response: {final_response_text}")

# Main async runner: create session first, then call agent
async def run_conversation():
    # create_session is async -> await here to ensure the session exists
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    print(f"Session created: App='{APP_NAME}', User='{USER_ID}', Session='{SESSION_ID}'")

    await call_agent_async("What is the weather like in London?", runner, USER_ID, SESSION_ID)
    await call_agent_async("How about Paris?", runner, USER_ID, SESSION_ID)
    await call_agent_async("Tell me the weather in New York", runner, USER_ID, SESSION_ID)

if __name__ == "__main__":
    try:
        asyncio.run(run_conversation())
    except Exception as e:
        print(f"An error occurred: {type(e).__name__}: {e}")
        raise
