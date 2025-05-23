from typing import List
from pydantic import BaseModel, Field

class CompanyRatingSummary(BaseModel):
    """Summary of average ratings for various aspects of a company based on employee reviews."""

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

class CompanyProCons(BaseModel):
    """List of commonly mentioned pros and cons in employee reviews of a company."""

    pros: List[str] = Field(..., description="Commonly mentioned positive aspects (pros) from employee reviews")
    cons: List[str] = Field(..., description="Commonly mentioned negative aspects (cons) from employee reviews")
