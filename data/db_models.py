from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, Boolean
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from database import base

class Company(base):
    __tablename__ = 'company'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    embedding = Column(Vector(768))

class EmploymentStatus(base):
    __tablename__ = 'employment_status'
    id = Column(Integer, primary_key=True,)
    status = Column(String, nullable=False, unique=True)
    is_current = Column(Boolean, nullable=False)

class EmploymentDuration(base):
    __tablename__ = 'employment_duration'
    id = Column(Integer, primary_key=True)
    duration = Column(String, nullable=False, unique=True)

class Opinion(base):
    __tablename__ = 'opinion'
    id = Column(Integer, primary_key=True)
    symbol = Column(String, nullable=False, unique=True)
    opinion = Column(String, nullable=False, unique=True)
    
class Review(base):
    __tablename__ = 'review'
    id = Column(Integer, primary_key=True)
    rating = Column(Integer)
    review_title = Column(Text)
    employment_status_id = Column(Integer, ForeignKey('employment_status.id'))
    employment_duration_id = Column(Integer, ForeignKey('employment_duration.id'))
    pros = Column(Text)
    cons = Column(Text)  
    recommended = Column(Boolean)  
    ceo_opinion_id = Column(Integer, ForeignKey('opinion.id'))
    business_outlook_opinion_id = Column(Integer, ForeignKey('opinion.id'))
    career_opportunities = Column(Integer)
    compensation_and_benefits = Column(Integer)
    senior_management = Column(Integer)
    work_life_balance = Column(Integer)
    culture_and_values = Column(Integer)
    diversity_and_inclusion = Column(Integer)
    company_id = Column(Integer, ForeignKey('company.id'), nullable=False)
    date = Column(Date)
    job_title = Column(Text)
    embedding = Column(Vector(768))
    
    company = relationship("Company")
    employment_status = relationship("EmploymentStatus")
    employment_duration = relationship("EmploymentDuration")  
    ceo_opinion = relationship("Opinion", foreign_keys=[ceo_opinion_id])
    business_outlook_opinion = relationship("Opinion", foreign_keys=[business_outlook_opinion_id])

    def print(self) -> None:
        summary_lines = [f"Review title: {self.review_title}"]
        if self.job_title is not None and self.job_title.strip():
            summary_lines.append(f"Reviewer Job title: {self.job_title}")
        if self.employment_status is not None:
            summary_lines.append(f"Employment status: {self.employment_status.status}")
        if self.employment_duration is not None:
            summary_lines.append(f"Employment duration: {self.employment_duration.duration}")   
        if self.rating is not None:
            summary_lines.append(f"General rating: {self.rating}/5")
        if self.pros is not None:
            summary_lines.append(f"Pros: {self.pros}")
        if self.cons is not None:
            summary_lines.append(f"Cons: {self.cons}")          
        if self.career_opportunities is not None:
            summary_lines.append(f"Career opportunities: {self.career_opportunities}/5")
        if self.compensation_and_benefits is not None:
            summary_lines.append(f"Compensation and benefits: {self.compensation_and_benefits}/5")
        if self.senior_management is not None:
            summary_lines.append(f"Senior management: {self.senior_management}/5")
        if self.work_life_balance is not None:
            summary_lines.append(f"Work-life balance: {self.work_life_balance}/5")
        if self.culture_and_values is not None:
            summary_lines.append(f"Culture and values: {self.culture_and_values}/5")
        if self.diversity_and_inclusion is not None:
            summary_lines.append(f"Diversity and inclusion: {self.diversity_and_inclusion}/5")      
        if self.recommended is not None:
            recommended_value = "Yes" if self.recommended == True else "No"   
            summary_lines.append(f"Recommended: {recommended_value}")      
        if self.ceo_opinion is not None:
            summary_lines.append(f"CEO Opinion: {self.ceo_opinion.opinion}")        
        if self.business_outlook_opinion is not None:
            summary_lines.append(f"Business Outlook: {self.business_outlook_opinion.opinion}")
            
        review_summary = "\n".join(summary_lines)
        print(review_summary)
