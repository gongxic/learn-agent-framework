import asyncio
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential, DefaultAzureCredential

agent = AzureOpenAIChatClient(credential=AzureCliCredential() ).create_agent(
    instructions="You are good at telling jokes.",
    name="Joker"
)

# Running the agent
# async def main():
#     result = await agent.run("Tell me a joke about a pirate.")
#     print(result.text)

# asyncio.run(main())

# Running the agent with streaming

async def main():
    async for update in agent.run_stream("Tell me a joke about a pirate."):
        if update.text:
            print(update.text, end="", flush=True)
    print()  # New line after streaming is complete


# Running the agent with a ChatMessage

# message = ChatMessage(
#     role=Role.USER,
#     contents=[
#         TextContent(text="Tell me a joke about this image?"),
#         UriContent(uri="https://samplesite.org/clown.jpg", media_type="image/jpeg")
#     ]
# )

# async def main():
#     result = await agent.run(message)
#     print(result.text)


if __name__ == "__main__":
    asyncio.run(main())