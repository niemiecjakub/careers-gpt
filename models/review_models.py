from typing import List
from pydantic import BaseModel, Field, ConfigDict, PrivateAttr
from pandas import DataFrame
from plotly.graph_objects import Figure

class CompanyRatingSummary(BaseModel):
    company_id: int = Field(..., description="Unique identifier for the company")
    company_name: str = Field(..., description="Name of the company")
    avg_general_rating: float = Field(..., description="Average overall rating given by employees")
    avg_career_opportunities_rating: float = Field(..., description="Average rating for career opportunities")
    avg_compensation_and_benefits_rating: float = Field(..., description="Average rating for compensation and benefits")
    avg_senior_management_rating: float = Field(..., description="Average rating for senior management")
    avg_work_life_balance_rating: float = Field(..., description="Average rating for work-life balance")
    avg_culture_and_values_rating: float = Field(..., description="Average rating for company culture and values")
    avg_diversity_and_inclusion_rating: float = Field(..., description="Average rating for diversity and inclusion")
    review_count: int = Field(..., description="Total number of reviews considered")

class CompanyProsCons(BaseModel):
    pros: List[str] = Field(..., description="Commonly mentioned positive aspects (pros) from employee reviews")
    cons: List[str] = Field(..., description="Commonly mentioned negative aspects (cons) from employee reviews")


class CompanyReviewQuestionResult(BaseModel):
    question: str = Field(..., description="Initial question about the company")
    proposed_questions: List[str] = Field(..., description="List of proposed follow-up questions")
    summary: str = Field(..., description="Summary of the retrieved data")
    sql: str = Field(..., description="SQL query to retrieve data from the database")
    
class CompanyReviewQuestionResultExtended(CompanyReviewQuestionResult):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    can_chart_be_generated: bool = Field(..., description="Whether a chart can be generated from the data")
    df: DataFrame = Field(..., exclude=True)
    fig: Figure = Field(..., exclude=True)
    
    