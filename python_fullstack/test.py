import asyncio
from llama_deploy.client import Client

async def main():

    client = Client(api_server_url="http://localhost:4501", timeout=10)

    # create a session (async)
    session = await client.core.sessions.create()

    # run your service
    result = await session.run("function_calling_agent", input="Hello from SG!")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())