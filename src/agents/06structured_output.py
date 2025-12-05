from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential
import asyncio
from pydantic import BaseModel
from agent_framework import AgentRunResponse

class PersonInfo(BaseModel):
    """Information about a person."""
    name: str | None = None
    age: int | None = None
    occupation: str | None = None

# Create the agent using Azure OpenAI Chat Client
agent = AzureOpenAIChatClient(credential=AzureCliCredential()).create_agent(
    name="HelpfulAssistant",
    instructions="You are a helpful assistant that extracts person information from text."
)

async def main():
    response = await agent.run(
        "Please provide information about John Smith, who is a 35-year-old software engineer.",
        response_format=PersonInfo
    )
    if response.value:
        person_info = response.value
        print(f"Name: {person_info.name}, Age: {person_info.age}, Occupation: {person_info.occupation}")
    else:
        print("No structured data found in response")


    # Get structured response from streaming agent using AgentRunResponse.from_agent_response_generator
    # This method collects all streaming updates and combines them into a single AgentRunResponse
    query="Please provide information about John Smith, who is a 35-year-old software engineer."
    final_response = await AgentRunResponse.from_agent_response_generator(
        agent.run_stream(query, response_format=PersonInfo),
        output_format_type=PersonInfo,
    )

    if final_response.value:
        person_info = final_response.value
        print(f"Name: {person_info.name}, Age: {person_info.age}, Occupation: {person_info.occupation}")


if __name__ == "__main__":
    asyncio.run(main())