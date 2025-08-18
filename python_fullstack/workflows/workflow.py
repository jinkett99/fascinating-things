# workflows/agent.py
import asyncio
from typing import Any, List

from llama_index.core.llms.function_calling import FunctionCallingLLM
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.tools.types import BaseTool
from llama_index.core.workflow import (
    Context,
    Workflow,
    StartEvent,
    StopEvent,
    step,
    Event
)
from llama_index.llms.openai import OpenAI
from llama_index.core.llms import ChatMessage
from llama_index.core.tools import ToolSelection, ToolOutput


# ---- Events
class InputEvent(Event):
    input: list[ChatMessage]


class StreamEvent(Event):
    delta: str


class ToolCallEvent(Event):
    tool_calls: list[ToolSelection]


class FunctionOutputEvent(Event):
    output: ToolOutput


# ---- Workflow
class FunctionCallingAgent(Workflow):
    def __init__(
        self,
        *args: Any,
        llm: FunctionCallingLLM | None = None,
        tools: List[BaseTool] | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.tools = tools or []
        # Construct LLM at runtime (NOT at import time)
        self.llm = llm or OpenAI(model="gpt-4o-mini", temperature=0.1, max_tokens=1024, streaming=True)
        assert self.llm.metadata.is_function_calling_model

    @step
    async def prepare_chat_history(self, ctx: Context, ev: StartEvent) -> InputEvent:
        await ctx.store.set("sources", [])
        memory = await ctx.store.get("memory", default=None)
        if not memory:
            memory = ChatMemoryBuffer.from_defaults(llm=self.llm)

        user_msg = ChatMessage(role="user", content=ev.input)
        memory.put(user_msg)
        await ctx.store.set("memory", memory)
        return InputEvent(input=memory.get())

    @step
    async def handle_llm_input(self, ctx: Context, ev: InputEvent) -> ToolCallEvent | StopEvent:
        chat_history = ev.input
        final = None

        response_stream = await self.llm.astream_chat_with_tools(self.tools, chat_history=chat_history)
        async for response in response_stream:
            ctx.write_event_to_stream(StreamEvent(delta=response.delta or ""))
            final = response

        if final is None or final.message is None:
            return StopEvent(result="No response generated.")

        memory = await ctx.store.get("memory")
        memory.put(final.message)
        await ctx.store.set("memory", memory)

        tool_calls = self.llm.get_tool_calls_from_response(final, error_on_no_tool_call=False)
        if not tool_calls:
            sources = await ctx.store.get("sources", default=[])
            return StopEvent(result=str(final))
        return ToolCallEvent(tool_calls=tool_calls)

    @step
    async def handle_tool_calls(self, ctx: Context, ev: ToolCallEvent) -> InputEvent:
        tools_by_name = {tool.metadata.get_name(): tool for tool in self.tools}
        tool_msgs = []
        sources = await ctx.store.get("sources", default=[])

        for tool_call in ev.tool_calls:
            tool = tools_by_name.get(tool_call.tool_name)
            additional_kwargs = {"tool_call_id": tool_call.tool_id, "name": tool.metadata.get_name() if tool else tool_call.tool_name}

            if not tool:
                tool_msgs.append(ChatMessage(role="tool", content=f"Tool {tool_call.tool_name} does not exist", additional_kwargs=additional_kwargs))
                continue

            try:
                tool_output = tool(**tool_call.tool_kwargs)
                sources.append(tool_output)
                tool_msgs.append(ChatMessage(role="tool", content=tool_output.content, additional_kwargs=additional_kwargs))
            except Exception as e:
                tool_msgs.append(ChatMessage(role="tool", content=f"Encountered error in tool call: {e}", additional_kwargs=additional_kwargs))

        memory = await ctx.store.get("memory")
        for msg in tool_msgs:
            memory.put(msg)

        await ctx.store.set("sources", sources)
        await ctx.store.set("memory", memory)
        return InputEvent(input=memory.get())

agent_workflow = FunctionCallingAgent(timeout=120)

async def main():
    print(await agent_workflow.run(input="Hello!"))

if __name__ == "__main__":
    asyncio.run(main())

# # ---- Factory (callable that returns a Workflow instance)
# def agent_workflow() -> FunctionCallingAgent:
#     agent = FunctionCallingAgent(timeout=120)
#     return agent