from typing import Annotated
from pydantic import Field
import asyncio
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential

def get_weather(
    location: Annotated[str, Field(description="The location to get the weather for.")],
) -> str:
    """Get the weather for a given location."""
    return f"The weather in {location} is cloudy with a high of 15°C."


weather_agent = AzureOpenAIChatClient(credential=AzureCliCredential()).create_agent(
    name="WeatherAgent",
    description="An agent that answers questions about the weather.",
    instructions="You answer questions about the weather.",
    tools=get_weather
)

# Convert agent to tool with custom parameters
weather_tool = weather_agent.as_tool(
    name="WeatherLookup",
    description="Look up weather information for any location",
    arg_name="query",
    arg_description="The weather query or location"
)

main_agent = AzureOpenAIChatClient(credential=AzureCliCredential()).create_agent(
    instructions="You are a helpful assistant who responds in Chinese.",
    tools=weather_tool
)


async def main():
    result = await main_agent.run("What is the weather like in Amsterdam?")
    print(result.text)


if __name__ == "__main__":
    asyncio.run(main())