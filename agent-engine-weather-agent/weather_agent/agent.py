from google.adk.agents import Agent
import requests
from vertexai.agent_engines import AdkApp

def get_weather(location: str) -> dict:
    """Returns the current weather for a given location."""

    # location geolocation lookup

    geolocation_api_response = requests.get("https://geocoding-api.open-meteo.com/v1/search",
                                        params={"name":location, "count": 1},
                                        timeout = 10 )

    parsed_geolocation_data = geolocation_api_response.json()

    if "results" not in parsed_geolocation_data or not parsed_geolocation_data["results"]:
        return {"error": f"could not find the location named {location}"}

    location_lat = parsed_geolocation_data["results"][0]["latitude"]
    location_lon = parsed_geolocation_data["results"][0]["longitude"]
    location_name = parsed_geolocation_data["results"][0]["name"]

    # weather lookup using returned geolocation

    weather_api_response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
        "latitude": location_lat,
        "longitude": location_lon,
        "current": "temperature_2m,precipitation,wind_speed_10m",
        },
        timeout=10,
    )

    parsed_weather_data = weather_api_response.json()
    current_weather_data = parsed_weather_data.get("current", {})

    # return current weather data to agent

    return{
        "location": location_name,
        "temperature": current_weather_data.get("temperature_2m"),
        "precipitation": current_weather_data.get("precipitation"),
        "wind_speed": current_weather_data.get("wind_speed_10m")
    }

root_agent = Agent(
    name="weather_agent",
    model="gemini-3.5-flash",
    description="Looks up the weather forcast for an area and offers advice.",
    instruction=(
        "You are a weather checking agent. When asked about the weather"
        "you use the get_weather tool, then explain the current weather and any"
        "personal precautions that might need to be taken based on the weather"
        "end every response with 'mic drop....'"
    ),
    tools=[get_weather],
)


app = AdkApp(agent=root_agent)