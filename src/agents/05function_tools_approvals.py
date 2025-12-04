from agent_framework import ChatMessage, Role
from agent_framework import ChatAgent
from agent_framework.openai import OpenAIResponsesClient
from agent_framework import ai_function
from typing import Annotated
import asyncio
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential, DefaultAzureCredential


@ai_function
def get_weather(location: Annotated[str, "The city and state, e.g. San Francisco, CA"]) -> str:
    """Get the current weather for a given location."""
    return f"The weather in {location} is cloudy with a high of 15°C."


@ai_function(approval_mode="always_require")
def get_weather_detail(location: Annotated[str, "The city and state, e.g. San Francisco, CA"]) -> str:
    """Get detailed weather information for a given location."""
    return f"The weather in {location} is cloudy with a high of 15°C, humidity 88%."


async def handle_approvals(query: str, agent) -> str:
    """Handle function call approvals in a loop."""
    current_input = query

    while True:
        result = await agent.run(current_input)

        if not result.user_input_requests:
            # No more approvals needed, return the final result
            return result.text

        # Build new input with all context
        new_inputs = [query]

        for user_input_needed in result.user_input_requests:
            print(
                f"Approval needed for: {user_input_needed.function_call.name}")
            print(f"Arguments: {user_input_needed.function_call.arguments}")

            # Add the assistant message with the approval request
            new_inputs.append(ChatMessage(
                role=Role.ASSISTANT, contents=[user_input_needed]))

            # Get user approval (in practice, this would be interactive)
            user_approval = True  # Replace with actual user input

            # Add the user's approval response
            new_inputs.append(
                ChatMessage(role=Role.USER, contents=[
                            user_input_needed.create_response(user_approval)])
            )

        # Continue with all the context
        current_input = new_inputs

# Usage


async def main():
    result_text = await handle_approvals("Get detailed weather for Seattle and Portland", agent)
    print(result_text)


# async def main():
#     async with ChatAgent(
#         chat_client=OpenAIResponsesClient(),
#         name="WeatherAgent",
#         instructions="You are a helpful weather assistant.",
#         tools=[get_weather, get_weather_detail],
#     ) as agent:
#         # Agent is ready to use

#         result = await agent.run("What is the detailed weather like in Amsterdam?")

#         if result.user_input_requests:
#             for user_input_needed in result.user_input_requests:
#                 print(f"Function: {user_input_needed.function_call.name}")
#                 print(
#                     f"Arguments: {user_input_needed.function_call.arguments}")

#         # Get user approval (in a real application, this would be interactive)
#         user_approval = True  # or False to reject

#         # Create the approval response
#         approval_message = ChatMessage(
#             role=Role.USER,
#             contents=[user_input_needed.create_response(user_approval)]
#         )

#         # Continue the conversation with the approval
#         final_result = await agent.run([
#             "What is the detailed weather like in Amsterdam?",
#             ChatMessage(role=Role.ASSISTANT, contents=[user_input_needed]),
#             approval_message
#         ])
#         print(final_result.text)


asyncio.run(main())
