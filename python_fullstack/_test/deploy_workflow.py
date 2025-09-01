from llama_deploy import (
    deploy_workflow,
    WorkflowServiceConfig,
    ControlPlaneConfig,
    SimpleMessageQueueConfig,
)
from llama_index.core.workflow import (
    Context,
    Event,
    Workflow,
    StartEvent,
    StopEvent,
    step,
)
from llama_index.llms.openai import OpenAI
# from llama_index.core.agent.workflow import FunctionAgent


class ProgressEvent(Event):
    progress: str


# create a dummy workflow
class MyWorkflow(Workflow):
    @step()
    async def run_step(self, ctx: Context, ev: StartEvent) -> StopEvent:
        # Initialize plain LLM (no function agent)
        llm = OpenAI(model="gpt-4o-mini", temperature=0)

        # Take arg1 from StartEvent
        arg1 = str(ev.get("arg1", ""))

        # Run the LLM directly
        response = await llm.acomplete(arg1)   # async completion

        # Convert to plain text
        text_output = getattr(response, "text", None) or str(response)

        # Stream progress
        ctx.write_event_to_stream(
            ProgressEvent(progress="LLM run complete")
        )

        return StopEvent(result=text_output)


async def main():
    await deploy_workflow(
        workflow=MyWorkflow(),
        workflow_config=WorkflowServiceConfig(
            host="127.0.0.1", port=8002, service_name="my_workflow"
        ),
        control_plane_config=ControlPlaneConfig(),
    )


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())