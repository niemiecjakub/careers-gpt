import os
import asyncio
from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion, OpenAIPromptExecutionSettings
from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from semantic_kernel.functions import KernelArguments
from plugins import CvPlugin, JobPlugin, SearchPlugin, CompanyReviewPlugin
from prompt_message import JOB_AGENT_SYSTEM_PROMPT

class Agent:

    def __init__(self):
        settings = OpenAIPromptExecutionSettings()
        settings.function_choice_behavior = FunctionChoiceBehavior.Auto()
        
        self.kernel = Kernel()
        self.kernel.add_service(OpenAIChatCompletion(api_key=os.getenv("OPENAI_API_KEY"),ai_model_id=os.getenv("CHAT_MODEL_ID")))
        self.kernel.add_plugin(CvPlugin(self.kernel), "cv_plgin")
        self.kernel.add_plugin(JobPlugin(self.kernel), "job_plugin")
        self.kernel.add_plugin(SearchPlugin(self.kernel), "search_plugin")
        self.kernel.add_plugin(CompanyReviewPlugin(self.kernel), "company_review_plugin")
        
        self.agent = ChatCompletionAgent(
            kernel=self.kernel,
            name="jobAssistant",
            instructions= JOB_AGENT_SYSTEM_PROMPT,
            arguments=KernelArguments(),
        )
    
    def run_conversation(self):
        async def conversation():
            thread : ChatHistoryAgentThread | None = None
            while True:
                input_text = input("User > ")
                print("Assistant > ",end="")
                async for response in self.agent.invoke_stream(messages=input_text, thread=thread):
                    print(response, end="")
                    thread = response.thread
                print(end="\n\n")
                
        asyncio.run(conversation())

    async def ask(self, message: str):
        answer = await self.agent.get_response(messages=message)
        return answer.content.content