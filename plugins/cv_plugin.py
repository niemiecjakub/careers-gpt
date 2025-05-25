import json
from typing import Annotated
from models import CvDocument
from services import PdfService, LatexService
from semantic_kernel.functions import kernel_function, KernelArguments, KernelFunctionFromPrompt
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import OpenAIChatPromptExecutionSettings
from prompt_message import CV_DATA_EXTRACTOR_PROMPT
from tools import spinner_async, spinner  
import streamlit as st

class CvPlugin:
    """Plugin for extracting CV data."""
    def __init__(self, kernel: Kernel):
        self.kernel = kernel
        
    @spinner_async("Extracting PDF data")
    @kernel_function(description="Retrives CV data from PDF file")
    async def extract_data_from_pdf(
        self, 
        filePath: Annotated[str, "The path to the PDF file"]
    ) -> Annotated[CvDocument, "The extracted CV data"]:
        """Extracts text from a PDF file."""  
        pdf_service = PdfService()
        cv_data = pdf_service.extract_data_from_pdf_path(filePath)

        settings = OpenAIChatPromptExecutionSettings()
        settings.response_format = CvDocument

        extract_data_function = KernelFunctionFromPrompt(
            prompt=CV_DATA_EXTRACTOR_PROMPT.format(input=cv_data),
            function_name="extract_data_from_pdf",
            description="Extracts text from a PDF file.",
        )

        response = await extract_data_function.invoke(kernel=self.kernel,arguments=KernelArguments(settings=settings))     
        return CvDocument.model_validate(json.loads(str(response)))
        
    @spinner("Preparing PDF file")    
    @kernel_function(description="""
        Export CV document as PDF file. 
        Returning True means that PDF file has been successfully crteated
        """)
    def export_cv_as_pdf(
        self, 
        cv: Annotated[CvDocument, "CV data model"],
        template_name: Annotated[str, "Template name. For default template use 'engineering'"],
        file_name: Annotated[str, "Output PDF filename without extension"],
    ) -> bool:
        latex_service = LatexService()
        latex = latex_service.generate_latex(template_name, cv)
        pdf_bytes = latex_service.render_pdf_file(latex, file_name)
        st.download_button(
            label="Download PDF",
            data=pdf_bytes,
            file_name=f"{file_name}.pdf",
            mime="application/pdf",
        )
    
        return True

 
    @spinner("Getting available CV templates")  
    @kernel_function(description="Get available CV template names")
    def get_template_names(self) -> Annotated[str, "CV PDF template names"]:
        return ["engineering"]
        
    