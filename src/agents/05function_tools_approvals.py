"""
Example: Using approval_mode for function calls that require user approval

This example demonstrates how to use @ai_function(approval_mode="always_require") 
decorator to create AI functions that require user approval before execution.
"""

import asyncio
from typing import Annotated
from agent_framework import ai_function, ChatAgent, ChatMessage, Role
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential


@ai_function
def get_weather(location: Annotated[str, "The city and state, e.g. San Francisco, CA"]) -> str:
    """Get the current weather for a given location."""
    return f"The weather in {location} is cloudy with a high of 15°C."


@ai_function(approval_mode="always_require")
def get_weather_detail(location: Annotated[str, "The city and state, e.g. San Francisco, CA"]) -> str:
    """Get detailed weather information for a given location. Requires user approval."""
    return f"The weather in {location} is cloudy with a high of 15°C, humidity 88%."


async def simple_approval_example(query: str, agent) -> str:
    """Simple example: single approval workflow"""
    print("=== Simple Approval Example ===\n")
    
    # First call - agent will request approval
    result = await agent.run(query)

    if result.user_input_requests:
        for user_input_needed in result.user_input_requests:
            print(f"Approval needed for function: {user_input_needed.function_call.name}")
            print(f"Arguments: {user_input_needed.function_call.arguments}\n")

        # In real applications, this should request user input
        user_approval = True  # True to approve, False to reject

        # Create approval response message
        approval_message = ChatMessage(
            role=Role.USER,
            contents=[user_input_needed.create_response(user_approval)]
        )

        # Continue conversation with approval
        final_result = await agent.run([
            query,
            ChatMessage(role=Role.ASSISTANT, contents=[user_input_needed]),
            approval_message
        ])
        return final_result.text
    
    return result.text


async def loop_approval_example(query: str, agent) -> str:
    """Example of handling multiple approval requests in a loop"""
    print("=== Loop Approval Example ===\n")
    
    current_input = query

    while True:
        result = await agent.run(current_input)

        if not result.user_input_requests:
            # No more approval requests, return final result
            return result.text

        # Build new input with all context
        new_inputs = [query]

        for user_input_needed in result.user_input_requests:
            print(f"Approval needed for: {user_input_needed.function_call.name}")
            print(f"Arguments: {user_input_needed.function_call.arguments}\n")

            # Add assistant message (contains approval request)
            new_inputs.append(
                ChatMessage(role=Role.ASSISTANT, contents=[user_input_needed])
            )

            # In real applications, this should request user input
            user_approval = True  # True to approve, False to reject

            # Add user's approval response
            new_inputs.append(
                ChatMessage(
                    role=Role.USER,
                    contents=[user_input_needed.create_response(user_approval)]
                )
            )

        # Continue with all context
        current_input = new_inputs


async def main():
    # Create agent with approval-required tools
    agent = AzureOpenAIChatClient(credential=AzureCliCredential()).create_agent(
        instructions="You are a helpful weather assistant.",
        tools=[get_weather, get_weather_detail]
    )

    # Run simple approval example
    result = await simple_approval_example("What is the detailed weather like in Amsterdam?", agent)
    print(f"Result: {result}\n")

    # Run loop approval example (handles multiple approval requests)
    result_text = await loop_approval_example(
        "Get detailed weather for Seattle and Portland",
        agent
    )
    print(f"Final result: {result_text}\n")


if __name__ == "__main__":
    asyncio.run(main())