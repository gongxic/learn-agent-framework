import asyncio
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity import AzureCliCredential

agent = AzureOpenAIChatClient(credential=AzureCliCredential()).create_agent(
    name="VisionAgent",
    instructions="You are a helpful agent that can analyze images"
)

from agent_framework import ChatMessage, TextContent, UriContent, Role

message = ChatMessage(
    role=Role.USER,
    contents=[
        TextContent(text="What do you see in this image?"),
        UriContent(
            uri="https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
            media_type="image/jpeg"
        )
    ]
)

# from agent_framework import ChatMessage, TextContent, DataContent, Role

# # Load image from local file
# with open("path/to/your/image.jpg", "rb") as f:
#     image_bytes = f.read()

# message = ChatMessage(
#     role=Role.USER,
#     contents=[
#         TextContent(text="What do you see in this image?"),
#         DataContent(
#             data=image_bytes,
#             media_type="image/jpeg"
#         )
#     ]
# )

async def main():
    result = await agent.run(message)
    print(result.text)


if __name__ == "__main__":
    asyncio.run(main())