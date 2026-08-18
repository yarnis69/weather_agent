import vertexai

client = vertexai.Client(  
    project="weather-agent-504614",
    location="europe-west2",
)

# list all deployed agents

all_agents = client.agent_engines.list()

print(list(all_agents))

# delete the Weather_Agent if it exists

client.agent_engines.delete(name=TBC, force=True)
