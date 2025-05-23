import pandas as pd
import os
import re
from typing import Optional, Sequence, Set
from db_models import base, Company, Review, EmploymentDuration, EmploymentStatus, Opinion
from data import engine, Session
from sqlalchemy import Column, text
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import math
import ollama
from dotenv import load_dotenv

class InitDatabase:
    
    def __init__(self, csv: str):
        if not os.path.exists(csv):
           raise FileNotFoundError(f"CSV file not found: {csv}")
        self.csv = csv 
        self.embedding_model = os.getenv("OLLAMA_EMBEDDING_MODEL")
        
    def __safe_str_to_int(self, value: str) -> Optional[int]:
        if value is None:
            return None
        try:
            f = float(value)
            if f.is_integer():
                return int(f)
            else:
                raise ValueError(f"Value {value} is not an integer")
        except ValueError:
            return None

    def __safe_int(self, value) -> Optional[int]:
        try:
            if value is None or (isinstance(value, float) and math.isnan(value)):
                return None
            return int(value)
        except Exception:
            return None

    def __safe_str(self, value) -> Optional[str]:
        if value is None:
            return None
        if isinstance(value, float) and math.isnan(value):
            return None
        return str(value)

    def __get_company_name(self, url: str) -> Optional[str]:
        pattern = r'(?:/|^)Reviews/([^/]+)-Reviews(?:-|$)'
        match = re.search(pattern, url)
        if match:
            return match.group(1).replace('-', ' ')
        print(f"COMPANY MISMATCH - {url}")
        return None

    def __get_employment_status(self, status: str) -> Optional[str]:
        try:
            if status is None or pd.isna(status):
                return None
            if not isinstance(status, str):
                status = str(status)
            return status.split(",")[0]
        except Exception as e:
            print(f"ERROR ON STATUS: {status} -> {e}")
            return None

    def __get_employment_duration(self, status: str) -> Optional[str]:
        try:
            if status is None or pd.isna(status):
                return None
            if not isinstance(status, str):
                status = str(status)
            statuses = status.split(",")
            if len(statuses) == 2:
                return statuses[1]
            return None
        except Exception as e:
            print(f"ERROR ON DURATION: {status} -> {e}")
            return None

    def __parse_date_string(self, date_str: str) -> Optional[datetime.date]:
        try:
            if date_str is None or pd.isna(date_str):
                return None
            if not isinstance(date_str, str):
                date_str = str(date_str)
            parsed = datetime.strptime(date_str.strip(), "%b %d, %Y")
            return parsed.date()
        except ValueError as e:
            print(f"Invalid date format: {date_str} -> {e}")
            return None

    def __create_embedding(self, input: str) -> Sequence[float]:
        embedding = ollama.embed(
            model=self.embedding_model, 
            input=input
        )    
        return embedding.embeddings[0]

    def __create_review_embedding(self, 
                                  review: Review, 
                                  employment_status : Optional[EmploymentStatus], 
                                  employment_duration:Optional[EmploymentDuration],
                                  opinion_map: dict[Column[str], Opinion]) -> Sequence[float]:
        summary_lines = [f"Review title: {review.review_title}"]
        if review.job_title is not None:
            summary_lines.append(f"Reviewer Job title: {review.job_title}")
        if employment_status is not None:
            summary_lines.append(f"Employment status: {employment_status.status}")
        if employment_duration is not None:
            summary_lines.append(f"Employment duration: {employment_duration.duration}")   
        if review.rating is not None:
            summary_lines.append(f"General rating: {review.rating}/5")
        if review.pros is not None:
            summary_lines.append(f"Pros: {review.pros}")
        if review.cons is not None:
            summary_lines.append(f"Cons: {review.cons}")          
        if review.career_opportunities is not None:
            summary_lines.append(f"Career opportunities: {review.career_opportunities}/5")
        if review.compensation_and_benefits is not None:
            summary_lines.append(f"Compensation and benefits: {review.compensation_and_benefits}/5")
        if review.senior_management is not None:
            summary_lines.append(f"Senior management: {review.senior_management}/5")
        if review.work_life_balance is not None:
            summary_lines.append(f"Work-life balance: {review.work_life_balance}/5")
        if review.culture_and_values is not None:
            summary_lines.append(f"Culture and values: {review.culture_and_values}/5")
        if review.diversity_and_inclusion is not None:
            summary_lines.append(f"Diversity and inclusion: {review.diversity_and_inclusion}/5")      
        if review.recommended is not None:
            recommended_value = "Yes" if review.recommended == True else "No"   
            summary_lines.append(f"Recommended: {recommended_value}")      
        if review.ceo_opinion_id is not None:
            ceo_opinion_value : Opinion = opinion_map.get(review.ceo_opinion_id, None)
            if ceo_opinion_value is not None:
                summary_lines.append(f"CEO Opinion: {ceo_opinion_value.opinion}")        
        if review.business_outlook_opinion_id is not None:
            business_outlook_opinion_value : Opinion = opinion_map.get(review.business_outlook_opinion_id, None)
            if business_outlook_opinion_value is not None:
                summary_lines.append(f"Business Outlook: {business_outlook_opinion_value.opinion}")
            
        review_summary = " | ".join(summary_lines)        
        return self.__create_embedding(review_summary)

    def __create_bool_opinion(self,value: Optional[str]) -> Optional[bool]:
        """From v/x/None create boolean value
        Applies for:
        - Recommended
        """
        value = self.__safe_str(value)
        if value == "v":
            return True
        if value == "x":
            return False
        return None
    
    def __create_opinion(self, opinions_map: dict, value: Optional[str]) -> Optional[int]:
        value = self.__safe_str(value)
        opinion = opinions_map.get(value, None)
        return opinion.id if opinion else None
    
    def initialize_tables(self) -> None:
        con = engine.connect()
        con.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        con.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm;"))
        con.commit()
        base.metadata.create_all(bind=engine)
                
    def insert_companies(self, create_embeddings : bool = False, chunksize : int = 100000) -> None:
        session = Session()
        seen_names = set()

        try:
            for chunk in pd.read_csv(self.csv, usecols=['firm_link'], chunksize=chunksize):
                chunk = chunk.dropna(subset=['firm_link'])

                company_names = {
                    self.__get_company_name(url)
                    for url in chunk['firm_link'].unique()
                    if self.__get_company_name(url) is not None
                }

                new_names = company_names - seen_names
                seen_names.update(new_names)

                if new_names:
                    companies = [
                        Company(name=name, embedding=self.__create_embedding(name) if create_embeddings else None)
                        for name in new_names
                    ]
                    session.bulk_save_objects(companies)
                    session.commit()

        except IntegrityError:
            session.rollback()
            
        finally:
            session.close()
            
    def insert_employment_statuses(self, chunksize : int = 100000) -> None:
        session = Session()
        seen_employment_status_names = set()
        seen_employment_duration_names = set()

        try:
            for chunk in pd.read_csv(self.csv, usecols=['status'], chunksize=chunksize):
                chunk = chunk.dropna(subset=['status'])
                unique_status_entries = set(chunk['status'].unique())

                new_employment_status_names : Set[str] = set()
                new_employment_duration_names: Set[str] = set()

                for raw_status in unique_status_entries:
                    employment_status_name = self.__get_employment_status(raw_status)
                    if employment_status_name and employment_status_name not in seen_employment_status_names:
                        new_employment_status_names.add(employment_status_name)
                        seen_employment_status_names.add(employment_status_name)

                    employment_duration_name = self.__get_employment_duration(raw_status)
                    if employment_duration_name and employment_duration_name not in seen_employment_duration_names:
                        new_employment_duration_names.add(employment_duration_name)
                        seen_employment_duration_names.add(employment_duration_name)

                if new_employment_status_names:
                    session.bulk_save_objects([
                        EmploymentStatus(
                            status=status_name,
                            is_current=status_name.lower().startswith("current")
                        ) 
                        for status_name in new_employment_status_names
                    ])
                    session.commit()

                if new_employment_duration_names:
                    session.bulk_save_objects([
                        EmploymentDuration(duration=duration_name) for duration_name in new_employment_duration_names
                    ])
                    session.commit()

        except IntegrityError:
            session.rollback()

        finally:
            session.close()
         
    def insert_opinions(self) -> None:
        opinions = {
            'v': 'Positive',
            'r': 'Mild',
            'x': 'Negative',
            'o': 'No opinion'
        }  
           
        session = Session()
        session.bulk_save_objects([
            Opinion(symbol=symbol, opinion=opinion) for symbol, opinion in opinions.items()
        ])   
             
        session.commit()
                
    def insert_reviews(self, create_embeddings : bool = False, chunksize : int = 1000,) -> None:
        batch_number = 0  
        session = Session()
        
        opinions = session.query(Opinion).all()
        opinions_map= {op.symbol: op for op in opinions} 
        
        try:
            for chunk in pd.read_csv(self.csv, chunksize=chunksize, on_bad_lines="warn", low_memory=False):  
                batch_number += 1
                review_objects = []

                print(f"BATCH {batch_number} - PROCESSING")
                for idx, row in chunk.iterrows():     
                    try:
                        company_name = self.__get_company_name(row["firm_link"])
                        employment_status_name = self.__get_employment_status(row["status"])
                        employment_duration_name = self.__get_employment_duration(row["status"])

                        company = session.query(Company).filter_by(name=company_name).first()
                        if company is None:
                            continue
                        
                        employment_status = session.query(EmploymentStatus).filter_by(status=employment_status_name).first()
                        employment_duration = session.query(EmploymentDuration).filter_by(duration=employment_duration_name).first()
                        
                        review = Review(
                            rating=self.__safe_int(row["rating"]),
                            review_title=self.__safe_str(row["title"]),
                            employment_status_id=employment_status.id if employment_status else None,
                            employment_duration_id=employment_duration.id if employment_duration else None,
                            pros=self.__safe_str(row["pros"]),
                            cons=self.__safe_str(row["cons"]),
                            recommended=self.__create_bool_opinion(row["Recommend"]),
                            ceo_opinion_id=self.__create_opinion(opinions_map, row["CEO Approval"]),
                            business_outlook_opinion_id=self.__create_opinion(opinions_map, row["Business Outlook"]),                
                            career_opportunities=self.__safe_str_to_int(row["Career Opportunities"]),
                            compensation_and_benefits=self.__safe_str_to_int(row["Compensation and Benefits"]),
                            senior_management=self.__safe_str_to_int(row["Senior Management"]),
                            work_life_balance=self.__safe_str_to_int(row["Work/Life Balance"]),
                            culture_and_values=self.__safe_str_to_int(row["Culture & Values"]),
                            diversity_and_inclusion=self.__safe_str_to_int(row["Diversity & Inclusion"]),
                            company_id=company.id if company else None,
                            date=self.__parse_date_string(row["date"]),
                            job_title=self.__safe_str(row["job"]),
                        )
                        if create_embeddings:
                            review.embedding = self.__create_review_embedding(
                                review=review, 
                                employment_status=employment_status, 
                                employment_duration=employment_duration, 
                                opinion_map=opinions_map)

                        review_objects.append(review)

                    except Exception as e:
                        print(f"Error on row index {idx}: {e}")

                if review_objects:
                    session.bulk_save_objects(review_objects)
                    session.commit()

        except IntegrityError as e:
            print(f"Commit failed: {e}")
            session.rollback()

        finally:
            session.close() 
        

    
def initialize_db():
    db = InitDatabase(os.getenv("CSV_INITIALIZATION_PATH"))
    db.initialize_tables()
    db.insert_employment_statuses()
    db.insert_companies(create_embeddings=False)
    db.insert_opinions()
    db.insert_reviews(create_embeddings=False)
    
load_dotenv()
initialize_db()
