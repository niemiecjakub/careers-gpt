import os
import asyncio
from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion, OpenAIPromptExecutionSettings
from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from semantic_kernel.functions import KernelArguments
from plugins import CvPlugin, JobPlugin, SearchPlugin, CompanyReviewPlugin
from prompt_message import JOB_AGENT_SYSTEM_PROMPT

async def main():

    settings = OpenAIPromptExecutionSettings()
    settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

    kernel = Kernel()
    kernel.add_service(OpenAIChatCompletion(api_key=os.getenv("OPENAI_API_KEY"),ai_model_id=os.getenv("CHAT_MODEL_ID")))
    kernel.add_plugin(CvPlugin(kernel), "cv_plgin")
    kernel.add_plugin(JobPlugin(kernel), "job_plugin")
    kernel.add_plugin(SearchPlugin(kernel), "search_plugin")
    kernel.add_plugin(SearchPlugin(kernel), "search_plugin")
    kernel.add_plugin(CompanyReviewPlugin(kernel), "company_review_plugin")
    
    agent = ChatCompletionAgent(
        kernel=kernel,
        name="jobAssistant",
        instructions= JOB_AGENT_SYSTEM_PROMPT,
        arguments=KernelArguments(),
    )

    thread : ChatHistoryAgentThread | None = None

    while True:
        input_text = input("User > ")
        print("Assistant > ",end="")
        async for response in agent.invoke_stream(messages=input_text, thread=thread):
            print(response, end="")
            thread = response.thread
        print(end="\n\n")

load_dotenv() 
asyncio.run(main())