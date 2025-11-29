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

async def run_conversation():
    global runner, session_service, root_agent, gemini_model
    
    # Create the Gemini model instance first
    gemini_model = Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config)
    
    # Initialize components
    chatbot_agent = Agent(
        model=gemini_model,
        name="text_chat_bot",
        description="A text chatbot",
    )
    
    # Re-define our app with Events Compaction enabled
    research_app_compacting = App(
        name="research_app_compacting",
        root_agent=chatbot_agent,
        # This is the new part!
        events_compaction_config=EventsCompactionConfig(
            compaction_interval=3,  # Trigger compaction every 3 invocations
            overlap_size=1,  # Keep 1 previous turn for context
        ),
    )

    print(f"Agent '{chatbot_agent.name}' created using model '{AGENT_MODEL}'.")

    # Step 2: Switch to DatabaseSessionService
    # SQLite database will be created automatically
    db_url = "sqlite:///my_agent_data.db"  # Local SQLite file
    session_service = DatabaseSessionService(db_url=db_url)

    research_runner_compacting = Runner(
        app=research_app_compacting, session_service=session_service
    )
    
    print("✅ Research App upgraded with Events Compaction!")


    print("✅ Upgraded to persistent sessions!")
    print(f"   - Database: my_agent_data.db")
    print(f"   - Sessions will survive restarts!")

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
            research_runner_compacting,
            "What is the latest news about AI in healthcare?",
            "compaction_demo",
        )

        # Turn 2
        await run_session(
            research_runner_compacting,
            "Are there any new developments in drug discovery?",
            "compaction_demo",
        )

        # Turn 3 - Compaction should trigger after this turn!
        await run_session(
            research_runner_compacting,
            "Tell me more about the second development you found.",
            "compaction_demo",
        )

        # Turn 4
        await run_session(
            research_runner_compacting,
            "Who are the main companies involved in that?",
            "compaction_demo",
        )
    # Turn 1

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