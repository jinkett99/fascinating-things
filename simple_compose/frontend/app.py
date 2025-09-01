import json

import chainlit as cl
from llama_deploy import LlamaDeployClient, ControlPlaneConfig

# Create a client to interact with the deployed system
client = LlamaDeployClient(ControlPlaneConfig(host="localhost", port=8000))

@cl.on_chat_start
async def on_chat_start():
    session = client.create_session()
    cl.user_session.set("session", session)
    cl.user_session.set("history", [])
    await cl.Message("Hi! How can I help you?").send()
    
@cl.on_message
async def on_chat_message(message: cl.Message):
    session = cl.user_session.get("session")
    history = cl.user_session.get("history")
    if history == []:
        result = session.run("my_workflow", task=message.content)
    else:
        result = session.run("my_workflow", task=message.content, chat_history=history)
    try:
        response, history = result.split(" ||History||: ")[0], json.loads(result.split(" ||History||: ")[1])
        cl.user_session.set("history", history)
        await cl.Message(response).send()
    except:
        cl.user_session.set("history", {"role": "assistant", "content": result})
        await cl.Message(result).send()