import uuid
from google.genai import types

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini


from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

from google.adk.apps.app import App, ResumabilityConfig
from google.adk.tools.function_tool import FunctionTool

print("✅ ADK components imported successfully.")
IMAGE_THRESHOLD = 1

retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)

# Image generation tool using MCP
mcp_image_server = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="npx",  # Run MCP server via npx
            args=[
                "-y",  # Argument for npx to auto-confirm install
                "@modelcontextprotocol/server-everything",
            ],
            tool_filter=["getTinyImage"],
        ),
        timeout=30,
    )
)

def call_image_generation(
    num_images: int,  tool_context: ToolContext
) -> dict:
    """Generates an image. Requires approval if ordering more than 1 iamges (IMAGE_THRESHOLD).

    Args:
        num_images: Number of images to generate

    Returns:
        Dictionary with image status
    """

    # -----------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------
    # SCENARIO 1: Small orders (≤5 containers) auto-approve
    if num_images <= IMAGE_THRESHOLD:
        return {
            "status": "approved",
            "generation_id": f"ORD-{num_images}-AUTO",
            "num_images": num_images,
            "message": f"Image generation auto-approved: {num_images} images ",
        }

    # -----------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------
    # SCENARIO 2: This is the first time this tool is called. Large orders need human approval - PAUSE here.
    if not tool_context.tool_confirmation:
        tool_context.request_confirmation(
            hint=f"⚠️ Large generation: {num_images} images to generate. Do you want to approve?",
            payload={"num_images": num_images},
        )
        return {  # This is sent to the Agent
            "status": "pending",
            "message": f"Generation for {num_images} images requires approval",
        }

    # -----------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------
    # SCENARIO 3: The tool is called AGAIN and is now resuming. Handle approval response - RESUME here.
    if tool_context.tool_confirmation.confirmed:
        return {
            "status": "approved",
            "generation_id": f"ORD-{num_images}-HUMAN",
            "num_images": num_images,
            
            "message": f"Generation approved: {num_images} images",
        }
    else:
        return {
            "status": "rejected",
            "message": f"Generation rejected: {num_images} images",
        }
        


# Create shipping agent with pausable tool
root_agent = LlmAgent(
    name="root_agent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""You are a image generator assistant.
  
  When users request to generate images:
   1. Use the call_image_generation tool with the number of images
   2. If the generation status is 'pending', inform the user that approval is required
   3. After receiving the final result, Use the MCP Tool to generate images for user queries
  """,
    tools=[mcp_image_server,FunctionTool(func=call_image_generation)],
)






