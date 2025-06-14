from semantic_kernel import Kernel
from semantic_kernel.functions import kernel_function
from typing import Annotated, Optional, List
from models import CompanyProsCons, CompanyRatingSummary
from models.review_models import CompanyReviewQuestionResult
from services import CompanyReviewService
from tools import spinner
import streamlit as st

class CompanyReviewPlugin:
    """Plugin for extracting company review data."""
    
    def __init__(self, kernel: Kernel):
        self.kernel = kernel

    @spinner("Getting company rating from the database")  
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
 
    @spinner("Getting pros & cons from the database")     
    @kernel_function(description="Retrieve aggregated pros and cons from employee reviews for a given company.")
    def get_company_pros_cons(
        self, 
        company_name: Annotated[str, "The name of the company to retrieve pros and cons for."],
        employee_status: Annotated[
            Optional[bool],
            "Filter reviews by employee status. Use True for current employees only, False for former employees only, or None to include all."
        ] = None
    ) -> Annotated[CompanyProsCons, "Aggregated pros and cons for the specified company."]:
        company_review_service = CompanyReviewService()
        company_id = company_review_service.get_company_id_by_name(company_name)
        company_pros_cons = company_review_service.get_company_pros_cons(
            company_id=company_id, 
            current_employee=employee_status
        )
        return CompanyProsCons(
            cons=company_pros_cons.cons[:30],   
            pros=company_pros_cons.pros[:30]
        )
        
    @spinner("Querying company review database")
    @kernel_function(description="Ask question to emplyee company reviews database.")
    def query_company_review_db(
        self, 
        question: Annotated[str, "A question about a company."] 
    ) -> Annotated[CompanyReviewQuestionResult, "Retrieved data from the company reviews database, including proposed follow-up questions and a summary."]:
        company_review_service = CompanyReviewService()   
        result = company_review_service.query_company_review_db(question)
        
        st.dataframe(result.df, use_container_width=True)  
        if (result.can_chart_be_generated):
            st.plotly_chart(result.fig, use_container_width=True)
            
        return CompanyReviewQuestionResult(
            question=result.question,
            summary=result.summary,
            proposed_questions=result.proposed_questions,
            sql=result.sql
        )
    
    @spinner("Thnking about similar questions")
    @kernel_function(description="Propose similar questions.")
    def get_similar_questions(
        self, 
        question: Annotated[str, "A question to which look for similar ones."] 
    ) -> Annotated[List[str], "Retrieved data from the company reviews database, including proposed follow-up questions and a summary."]:
        company_review_service = CompanyReviewService()   
        return company_review_service.get_similar_questions(question)

    