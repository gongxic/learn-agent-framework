from agent_framework import ai_function
from pydantic import Field
from typing import Annotated
import asyncio
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential


@ai_function(name="weather_tool", description="Retrieves weather information for any location")
def get_weather(
    location: Annotated[str, Field(description="The location to get the weather for.")],
) -> str:
    return f"The weather in {location} is cloudy with a high of 15°C."


weather_agent = AzureOpenAIChatClient(credential=AzureCliCredential()).create_agent(
    instructions="You are a helpful assistant",
    tools=get_weather
)

class WeatherTools:
    def __init__(self):
        self.last_location = None

    def get_weather(
        self,
        location: Annotated[str, Field(description="The location to get the weather for.")],
    ) -> str:
        """Get the weather for a given location."""
        return f"The weather in {location} is cloudy with a high of 15°C."

    def get_weather_details(self) -> int:
        """Get the detailed weather for the last requested location."""
        if self.last_location is None:
            return "No location specified yet."
        return f"The detailed weather in {self.last_location} is cloudy with a high of 15°C, low of 7°C, and 60% humidity."


tools = WeatherTools()
main_agent = AzureOpenAIChatClient(credential=AzureCliCredential()).create_agent(
    instructions="You are a helpful assistant",
    tools=[tools.get_weather, tools.get_weather_details]
)


async def main():

    result = await weather_agent.run("What is the weather like in Amsterdam?")
    print(result.text)
    result = await main_agent.run("What is the weather like in Amsterdam?")
    print(result.text)


asyncio.run(main())
