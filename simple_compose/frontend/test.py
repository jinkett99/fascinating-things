import asyncio
from llama_index.core.workflow import Context
from llama_deploy import LlamaDeployClient, ControlPlaneConfig

async def main():
    # Connect to the control plane exposed on localhost:8000
    client = LlamaDeployClient(
        ControlPlaneConfig(host="localhost", port=8000)
    )

    # Create a session
    session = client.create_session()

    # set Context to store history
    ctx = Context(session)

    # Run against the deployed workflow
    result = session.run("my_workflow", input="Hello from Singapore!", ctx=ctx)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
