# app.py
import json
import chainlit as cl
from llama_deploy import AsyncLlamaDeployClient  # <- API server client
from llama_deploy.control_plane.server import ControlPlaneConfig

# Set up control plane configuration
control_plane_config = ControlPlaneConfig(host="0.0.0.0", port=8000)

client = AsyncLlamaDeployClient(control_plane_config=control_plane_config, timeout=15)

@cl.on_chat_start
async def on_chat_start():
    # ensure deployment exists: "MyDeployment" from python_fullstack.yaml:name
    session = client.get_or_create_session("MyDeployment")
    cl.user_session.set("session", session)
    cl.user_session.set("history", [])
    await cl.Message("Hi! How can I help you?").send()

@cl.on_message
async def on_chat_message(message: cl.Message):
    session = cl.user_session.get("session")
    history = cl.user_session.get("history", [])
    # service matches `default-service` / `services` key: "function_calling_agent"
    result = session.run(
        service="function_calling_agent",
        input=message.content,
        chat_history=history if history else None,
    )
    try:
        response, history = result.split(" ||History||: ")[0], json.loads(result.split(" ||History||: ")[1])
        cl.user_session.set("history", history)
        await cl.Message(response).send()
    except Exception:
        cl.user_session.set("history", [{"role": "assistant", "content": result}])
        await cl.Message(result).send()
