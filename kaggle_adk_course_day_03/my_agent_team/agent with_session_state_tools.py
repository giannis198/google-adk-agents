# fixed_with_env.py
import os
import asyncio
from dotenv import load_dotenv
import warnings
warnings.filterwarnings("ignore")
import logging
logging.basicConfig(level=logging.ERROR)

from typing import Any, Dict

from google.adk.agents import Agent, LlmAgent
from google.adk.apps.app import App, EventsCompactionConfig
from google.adk.models.google_llm import Gemini
from google.adk.sessions import DatabaseSessionService
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.tools.tool_context import ToolContext
from google.genai import types

print("✅ ADK components imported successfully.")

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
MODEL_GEMINI_2_0_FLASH = "gemini-2.5-flash-lite"
AGENT_MODEL = MODEL_GEMINI_2_0_FLASH
APP_NAME = "default"  # Application
USER_ID = "default"  # User
SESSION = "default"  # Session

async def run_session(
    runner_instance: Runner,
    user_queries: list[str] | str = None,
    session_name: str = "default",
):
    print(f"\n ### Session: {session_name}")

    # Get app name from the Runner
    app_name = runner_instance.app_name

    # Attempt to create a new session or retrieve an existing one
    try:
        session = await session_service.create_session(
            app_name=app_name, user_id=USER_ID, session_id=session_name
        )
        print(f"✅ Created new session: {session_name}")
    except Exception as e:
        # If session already exists, get the existing one
        if "already exists" in str(e):
            session = await session_service.get_session(
                app_name=app_name, user_id=USER_ID, session_id=session_name
            )
            print(f"✅ Retrieved existing session: {session_name}")
        else:
            # Re-raise unexpected errors
            raise

    # Process queries if provided
    if user_queries:
        # Convert single query to list for uniform processing
        if isinstance(user_queries, str):
            user_queries = [user_queries]

        # Process each query in the list sequentially
        for raw_query in user_queries:
            print(f"\nUser > {raw_query}")

            # Convert the query string to the ADK Content format
            query_content = types.Content(role="user", parts=[types.Part(text=raw_query)])

            final_response_text = "Agent did not produce a final response."

            # Stream the agent's response asynchronously
            async for event in runner_instance.run_async(
                user_id=USER_ID, session_id=session.id, new_message=query_content
            ):
                # If event contains content, print partial/streamed text (filter out empty/"None")
                if getattr(event, "content", None) and getattr(event.content, "parts", None):
                    part_text = event.content.parts[0].text
                    if part_text and part_text != "None":
                        print(f"{AGENT_MODEL} > ", part_text)

                # Check for final response (mirror logic from call_agent_async)
                if getattr(event, "is_final_response", lambda: False)() :
                    if getattr(event, "content", None) and getattr(event.content, "parts", None):
                        final_response_text = event.content.parts[0].text
                    elif getattr(event, "actions", None) and getattr(event.actions, "escalate", False):
                        final_response_text = f"Agent escalated: {getattr(event, 'error_message', 'No specific message.')}"
                    break

            print(f"<<< Agent Response: {final_response_text}")
    else:
        print("No queries!")

print("✅ Helper functions defined.")

retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)

# Global variables for cleanup
runner = None
session_service = None
root_agent = None
gemini_model = None

async def close_all_http_clients():
    """Force close all aiohttp clients and sessions"""
    import aiohttp
    import gc
    
    print("🔍 Searching for unclosed aiohttp sessions...")
    
    # Force close all aiohttp ClientSessions
    for obj in gc.get_objects():
        try:
            if isinstance(obj, aiohttp.ClientSession):
                if not obj.closed:
                    await obj.close()
                    print("✅ Force-closed aiohttp ClientSession")
        except:
            pass
    
    # Close default session if it exists
    try:
        await aiohttp.ClientSession().close()
    except:
        pass

async def cleanup():
    """Properly cleanup all resources"""
    global runner, session_service, root_agent, gemini_model
    
    print("\n🧹 Cleaning up resources...")
    
    # Close runner first
    if runner is not None:
        try:
            await runner.close()
            print("✅ Runner closed successfully")
        except Exception as e:
            print(f"⚠️ Warning: runner.close() raised: {type(e).__name__}: {e}")

    # Close model clients - more comprehensive approach
    if root_agent is not None:
        try:
            model = getattr(root_agent, "model", None)
            if model is not None:
                # Try multiple approaches to close the Gemini client
                client_close_methods = [
                    # Method 1: Direct client access
                    lambda: getattr(model, '_client', None),
                    lambda: getattr(model, 'client', None),
                    lambda: getattr(model, '_live_api_client', None),
                    lambda: getattr(model, 'api_client', None),
                    
                    # Method 2: Look for transport/session
                    lambda: getattr(getattr(model, '_client', None), '_transport', None),
                    lambda: getattr(getattr(model, 'client', None), '_session', None),
                ]
                
                for method in client_close_methods:
                    try:
                        client = method()
                        if client is not None:
                            if hasattr(client, 'aclose'):
                                await client.aclose()
                                print(f"✅ Closed client using aclose(): {method.__name__}")
                            elif hasattr(client, 'close'):
                                client.close()
                                print(f"✅ Closed client using close(): {method.__name__}")
                    except Exception as e:
                        continue
                        
        except Exception as e:
            print(f"⚠️ Error during model cleanup: {e}")

    # Force close all HTTP clients
    await close_all_http_clients()
    
    # Additional cleanup: manually clear Gemini client cache
    try:
        from google.genai import client
        if hasattr(client, '_global_client'):
            del client._global_client
    except:
        pass


# Define scope levels for state keys (following best practices)
USER_NAME_SCOPE_LEVELS = ("temp", "user", "app")


# This demonstrates how tools can write to session state using tool_context.
# The 'user:' prefix indicates this is user-specific data.
def save_userinfo(
    tool_context: ToolContext, user_name: str, country: str
) -> Dict[str, Any]:
    """
    Tool to record and save user name and country in session state.

    Args:
        user_name: The username to store in session state
        country: The name of the user's country
    """
    # Write to session state using the 'user:' prefix for user data
    tool_context.state["user:name"] = user_name
    tool_context.state["user:country"] = country

    return {"status": "success"}


# This demonstrates how tools can read from session state.
def retrieve_userinfo(tool_context: ToolContext) -> Dict[str, Any]:
    """
    Tool to retrieve user name and country from session state.
    """
    # Read from session state
    user_name = tool_context.state.get("user:name", "Username not found")
    country = tool_context.state.get("user:country", "Country not found")

    return {"status": "success", "user_name": user_name, "country": country}


print("✅ Tools created.")

async def run_conversation():
    global runner, session_service, root_agent, gemini_model
    
    # Create the Gemini model instance first
    gemini_model = Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config)
    
    # Initialize components
    root_agent = LlmAgent(
        model=gemini_model,
        name="text_chat_bot",
        description="""A text chatbot.
    Tools for managing user context:
    * To record username and country when provided use `save_userinfo` tool. 
    * To fetch username and country when required use `retrieve_userinfo` tool.
    """,
    tools=[save_userinfo, retrieve_userinfo],  # Provide the tools to the agent
    )
    
   

    print(f"Agent '{root_agent.name}' created using model '{AGENT_MODEL}'.")

    session_service = InMemorySessionService()

    runner = Runner(agent=root_agent, session_service=session_service, app_name="default")

    print("✅ Agent with session state tools initialized!")

    # Create or get the session with proper error handling
    try:
        await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=SESSION
        )
        print(f"✅ Created new session: App='{APP_NAME}', User='{USER_ID}', Session='{SESSION}'")
    except Exception as e:
        if "already exists" in str(e):
            print(f"✅ Using existing session: App='{APP_NAME}', User='{USER_ID}', Session='{SESSION}'")
        else:
            # Re-raise unexpected errors
            raise

    try:
        # Turn 1
    # Turn 1
        await run_session(
    runner,
    [
        "Hi there, how are you doing today? What is my name?",  # Agent shouldn't know the name yet
        "My name is Sam. I'm from Poland.",  # Provide name - agent should save it
        "What is my name? Which country am I from?",  # Agent should recall from session state
    ],
    "state-demo-session",
)

       # Retrieve the session and inspect its state
        session = await session_service.get_session(
            app_name=APP_NAME, user_id=USER_ID, session_id="state-demo-session"
        )

        print("Session State Contents:")
        print(session.state)
        print("\n🔍 Notice the 'user:name' and 'user:country' keys storing our data!")

    except Exception as e:
        print(f"❌ Error during conversation: {type(e).__name__}: {e}")
        raise
    finally:
        # Ensure cleanup happens even if there's an error
        await cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(run_conversation())
    except KeyboardInterrupt:
        print("\n⚠️ Interrupted by user")
    except Exception as e:
        print(f"❌ An error occurred: {type(e).__name__}: {e}")
        # Try to cleanup even if main function fails
        try:
            asyncio.run(cleanup())
        except:
            pass
        raise
    finally:
        # Final cleanup pass
        try:
            asyncio.run(close_all_http_clients())
        except:
            pass
        
        # Force garbage collection
        import gc
        gc.collect()
        print("🎯 Script execution completed")