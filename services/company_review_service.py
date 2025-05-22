from typing import List, Optional
from sqlalchemy.orm import joinedload
from sqlalchemy import desc, func
from data import session, Company, Review, EmploymentStatus
from models import CompanyRatingSummary, CompanyProCons

class CompanyReviewService:

    def get_companies(self) -> List[Company]:
        """Return all companies."""
        with session() as s:
            return s.query(Company).all()

    def get_company_id_by_name(self, company_name: int) -> Optional[int]:
        """Return a company ID by its name."""
        with session() as s:
            return s.query(Company).filter(Company.name == company_name).first()

    def get_reviews_for_company(self, company_id: int, limit: int = 10) -> List[Review]:
        """Return reviews for a specific company."""
        with session() as s:
            return s.query(Review).options(
                joinedload(Review.employment_status),
                joinedload(Review.employment_duration),
                joinedload(Review.ceo_opinion),
                joinedload(Review.business_outlook_opinion)
            ).filter(Review.company_id == company_id).order_by(desc(Review.date)).limit(limit)

    def get_company_rating_summary(self, company_id: int, current_employee: Optional[bool] = None) -> CompanyRatingSummary:
        """Get detailed company rating"""
        with session() as s:
            query = s.query(
                Review.company_id,
                Company.name.label("company_name"),
                func.avg(Review.rating).label("avg_general_rating"),
                func.avg(Review.career_opportunities).label("avg_career_opportunities"),
                func.avg(Review.compensation_and_benefits).label("avg_compensation_and_benefits"),
                func.avg(Review.senior_management).label("avg_senior_management"),
                func.avg(Review.work_life_balance).label("avg_work_life_balance"),
                func.avg(Review.culture_and_values).label("avg_culture_and_values"),
                func.avg(Review.diversity_and_inclusion).label("avg_diversity_and_inclusion"),
                func.count(Review.id).label("review_count")
            ).join(Company) \
             .join(EmploymentStatus) \
             .filter(Review.company_id == company_id)

            if current_employee is not None:
                query = query.filter(EmploymentStatus.is_current == current_employee)

            result = query.group_by(Review.company_id, Company.name).one_or_none()

            if result is None:
                return None

            return CompanyRatingSummary(
                company_id=result.company_id,
                company_name=result.company_name,
                avg_general_rating=result.avg_general_rating,
                avg_career_opportunities_rating=result.avg_career_opportunities,
                avg_compensation_and_benefits_rating=result.avg_compensation_and_benefits,
                avg_senior_management_rating=result.avg_senior_management,
                avg_work_life_balance_rating=result.avg_work_life_balance,
                avg_culture_and_values_rating=result.avg_culture_and_values,
                avg_diversity_and_inclusion_rating=result.avg_diversity_and_inclusion,
                review_count=result.review_count
            )

    def get_company_pros_cons(self, company_id: int, current_employee: Optional[bool] = None) -> CompanyProCons:
        """Get pros and cons for company"""
        with session() as s:
            query = s.query(
                Review.pros,
                Review.cons
            ).join(Company) \
            .join(EmploymentStatus) \
            .filter(Review.company_id == company_id) \
                
            if current_employee is not None:
                query = query.filter(EmploymentStatus.is_current == current_employee)

            reviews = query.all()
            
            if not reviews:
                return None
            
            return CompanyProCons(
                pros=[review.pros for review in reviews],
                cons=[review.cons for review in reviews],
            )
            
# TODO: endpoints for extracting data summary (averages, medians) for company reviews
# TODO: company summary
