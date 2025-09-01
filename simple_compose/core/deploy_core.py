# ./core/deploy_core.py
from llama_deploy import deploy_core, ControlPlaneConfig
from llama_deploy.message_queues.redis import RedisMessageQueueConfig 
import asyncio

async def main():
    await deploy_core(
        control_plane_config=ControlPlaneConfig(host="0.0.0.0", port=8000),
        message_queue_config=RedisMessageQueueConfig(url="redis://redis:6379/0"),
    )

if __name__ == "__main__":
    asyncio.run(main())


