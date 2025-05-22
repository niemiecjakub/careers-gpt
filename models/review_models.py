from dataclasses import dataclass
from typing import List

@dataclass
class CompanyRatingSummary:
    company_id: int
    company_name: str
    avg_general_rating: float
    avg_career_opportunities_rating: float
    avg_compensation_and_benefits_rating: float
    avg_senior_management_rating: float
    avg_work_life_balance_rating: float
    avg_culture_and_values_rating: float
    avg_diversity_and_inclusion_rating: float
    review_count: int

@dataclass
class CompanyProCons:
    pros: List[str]
    cons: List[str]