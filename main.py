import os
import asyncio
from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion, OpenAIPromptExecutionSettings
from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from semantic_kernel.functions import KernelArguments
from plugins import CvPlugin, JobPlugin, SearchPlugin
from prompt_message import JOB_AGENT_SYSTEM_PROMPT


async def main():

    settings = OpenAIPromptExecutionSettings()
    settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

    kernel = Kernel()
    kernel.add_service(OpenAIChatCompletion(api_key=os.getenv("OPENAI_API_KEY"),ai_model_id=os.getenv("CHAT_MODEL_ID")))
    kernel.add_plugin(CvPlugin(kernel), "cv_plugin")
    kernel.add_plugin(JobPlugin(kernel), "job_plugin")
    kernel.add_plugin(SearchPlugin(kernel), "search_plugin")
    
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
# asyncio.run(main())

from services import LatexService
from models import CvDocument

import json
from models import CvDocument  # Make sure this points to your actual model file

# Sample JSON data as a string
cv_json = """
{
  "personal_details": {
    "name": "Jane Smith",
    "phone": "+1 555 123 4567",
    "email": "jane.smith@example.com",
    "location": "San Francisco, CA",
    "links": [
      {"name": "LinkedIn", "url": "https://linkedin.com/in/janesmith"},
      {"name": "GitHub", "url": "https://github.com/janesmith"}
    ]
  },
  "about_me": "Experienced software engineer with a passion for developing innovative programs that expedite the efficiency and effectiveness of organizational success.",
  "education": [
    {
      "degree": "Bachelor of Science in Computer Science",
      "institution": "Stanford University",
      "location": "Stanford, CA",
      "description": "Graduated with distinction, GPA: 3.9/4.0",
      "field_of_study": "Computer Science",
      "begin_date": "2014",
      "end_date": "2018"
    }
  ],
  "work_experience": [
    {
      "job_title": "Senior Software Engineer",
      "company": "Tech Innovators Inc.",
      "location": "San Jose, CA",
      "begin_date": "2020",
      "end_date": "Present",
      "description": "Leading backend development and system architecture design.",
      "responsibilities": [
        "Developed scalable microservices using Python and Docker.",
        "Designed and implemented cloud infrastructure on AWS.",
        "Mentored a team of junior developers."
      ]
    },
    {
      "job_title": "Software Engineer",
      "company": "Web Solutions LLC",
      "location": "Palo Alto, CA",
      "begin_date": "2018",
      "end_date": "2020",
      "description": "Built client-facing applications and internal tools.",
      "responsibilities": [
        "Created responsive UI with React and Redux.",
        "Improved application performance by 35%.",
        "Collaborated with cross-functional teams on feature development."
      ]
    }
  ],
  "skills": ["Python", "JavaScript", "React", "Django", "AWS", "Docker", "Git", "SQL"],
  "languages": ["English (Native)", "Spanish (Professional Proficiency)"],
  "other_sections": [
    {
      "title": "Certifications",
      "description": "Recognized industry certifications:",
      "details": [
        "AWS Certified Solutions Architect – Associate",
        "Certified ScrumMaster (CSM)"
      ]
    },
    {
      "title": "Projects",
      "description": "Notable open-source and personal projects:",
      "details": [
        "Developed an AI-based resume parser using NLP.",
        "Built a task automation bot with Selenium and Python."
      ]
    }
  ]
}
"""

cv_dict = json.loads(cv_json)
cv_document = CvDocument(**cv_dict)
latex = LatexService()
latex.generate_latex_file(cv_document)
