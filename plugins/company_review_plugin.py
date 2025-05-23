import os
import ollama
from semantic_kernel import Kernel
from semantic_kernel.functions import kernel_function, KernelArguments, KernelFunctionFromPrompt
from semantic_kernel.connectors.ai.open_ai import OpenAIChatPromptExecutionSettings
from typing import Annotated, Optional, List
from models import CompanyProCons, CompanyRatingSummary
from data.db_models import Company
from services import CompanyReviewService

class CompanyReviewPlugin:
    """Plugin for extracting company review data."""
    
    def __init__(self, kernel: Kernel):
        self.kernel = kernel

    @kernel_function(description="Retrieve the aggregated rating summary for a given company, including average ratings across categories and review count.")
    def get_company_rating(
        self,
        company_name: Annotated[str, "The name of the company to retrieve the rating summary for."],
        employee_status: Annotated[
            bool | None,
            "Filter reviews by employee status. Use True for current employees only, False for former employees only, or None to include all. Argument type is boolean or None"
        ] = None
    ) -> Annotated[CompanyRatingSummary, "Aggregated rating summary including category ratings and review count."]:
        company_review_service = CompanyReviewService()
        company_id = company_review_service.get_company_id_by_name(company_name)
        return company_review_service.get_company_rating_summary(
            company_id=company_id,
            current_employee=employee_status
        )
    
    @kernel_function(description="Retrieve aggregated pros and cons from employee reviews for a given company.")
    def get_company_pros_cons(
        self, 
        company_name: Annotated[str, "The name of the company to retrieve pros and cons for."],
        employee_status: Annotated[
            Optional[bool],
            "Filter reviews by employee status. Use True for current employees only, False for former employees only, or None to include all."
        ] = None
    ) -> Annotated[CompanyProCons, "Aggregated pros and cons for the specified company."]:
        company_review_service = CompanyReviewService()
        company_id = company_review_service.get_company_id_by_name(company_name)
        company_pros_cons = company_review_service.get_company_pros_cons(
            company_id=company_id, 
            current_employee=employee_status
        )
        return CompanyProCons(
            cons=company_pros_cons.cons[:30],
            pros=company_pros_cons.pros[:30]
        )