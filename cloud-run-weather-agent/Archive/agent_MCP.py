from google.adk.agents import Agent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

weather_toolset = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="npx",
            args=["-y", "@dangahagan/weather-mcp@latest"],
        ),
    ),
)

root_agent = Agent(
    name="weather_agent",
    model="gemini-3.6-flash",
    description="Looks up the weather forecast for an area and offers advice.",
    instruction=(
        "You are a weather checking agent. When asked about the weather, "
        "use the available weather tools to look up current conditions or "
        "forecasts, then explain the weather in plain English and any "
        "personal precautions that might need to be taken based on it. "
        "end every response with 'mic drop....'"
    ),
    tools=[weather_toolset],
)