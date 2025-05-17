import json
from typing import Annotated
from semantic_kernel import Kernel
from models.job_models import JobDocument
from semantic_kernel.functions import kernel_function, KernelArguments, KernelFunctionFromPrompt
from service.web_page_service import WebPageService
from semantic_kernel.connectors.ai.open_ai import OpenAIChatPromptExecutionSettings
from prompt_message import JOB_DATA_EXTRACTOR_PROMPT

class JobPlugin:
    """Plugin for extracting job data."""
    def __init__(self, kenrel : Kernel):
        self.kenrel = kenrel

    @kernel_function(description="Retrieves job data from a web page")
    async def extract_job_data_from_web_page(
        self, 
        url: str) -> Annotated[JobDocument, "The extracted job data"]:
        """Extracts job data from a web page."""
        web_page_service = WebPageService()
        job_data = web_page_service.get_html_content(url)

        settings = OpenAIChatPromptExecutionSettings()
        settings.response_format = JobDocument

        extract_data_function = KernelFunctionFromPrompt(
            prompt=JOB_DATA_EXTRACTOR_PROMPT.format(input=job_data),
            function_name="extract_data_from_web_page",
            description="Extracts job data from web page.",
        )

        response = await extract_data_function.invoke(kernel=self.kenrel, arguments=KernelArguments(settings=settings))
        return JobDocument.model_validate(json.loads(str(response)))