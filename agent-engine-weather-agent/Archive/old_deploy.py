import vertexai
from vertexai import agent_engines
from vertexai.preview import reasoning_engines
from weather_agent.agent import root_agent

vertexai.init(
    project="weather-agent-504614",
    location="europe-west2",
    staging_bucket="gs://weather-agent-504614-agent-staging",
)

app = reasoning_engines.AdkApp(agent=root_agent, enable_tracing=True)

remote_app = agent_engines.create(
    agent_engine=app,
    display_name="Weather Agent",
    requirements="./weather_agent/requirements.txt",
    extra_packages=["./weather_agent"],
)

print(remote_app.resource_name)