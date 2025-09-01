import asyncio
from llama_deploy import LlamaDeployClient, ControlPlaneConfig

async def main():

    # points to deployed control plane
    client = LlamaDeployClient(ControlPlaneConfig())
    session = client.create_session()
    result = session.run("my_workflow", arg1="Hello_from_SG")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())