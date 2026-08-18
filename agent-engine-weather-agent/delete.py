import vertexai

client = vertexai.Client(  
    project="weather-agent-504614",
    location="europe-west2",
)

# list all deployed agents

all_agents = client.agent_engines.list()

# find Weather_Agent by display name and assign to target_agent variable

target_agent = next(
    (agent for agent in all_agents if agent.display_name == "Weather_Agent"),
    None
)

# delete the Weather_Agent if it exists

client.agent_engines.delete(name=target_agent.api_resource.name, force=True)
