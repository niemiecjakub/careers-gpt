from sqlalchemy import Column, Integer, String, ForeignKey, Date, Text, Boolean, Enum
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from database import Base

class Company(Base):
    __tablename__ = 'company'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

class EmploymentStatus(Base):
    __tablename__ = 'employment_status'
    id = Column(Integer, primary_key=True,)
    status = Column(String, nullable=False, unique=True)

class EmploymentDuration(Base):
    __tablename__ = 'employment_duration'
    id = Column(Integer, primary_key=True)
    duration = Column(String, nullable=False, unique=True)

class Opinion(Base):
    __tablename__ = 'opinion'
    id = Column(Integer, primary_key=True)
    symbol = Column(String, nullable=False, unique=True)
    opinion = Column(String, nullable=False, unique=True)
    
class Review(Base):
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
