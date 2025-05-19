import pandas as pd
import re
from typing import Optional
from db_models import Base,Company, Review, EmploymentDuration, EmploymentStatus
from database import engine, SessionLocal

from sqlalchemy.exc import IntegrityError
from datetime import datetime
import math

class InitDatabase:
    def __init__(self, csv: str):
        self.csv = csv 
    
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

    def create_tables(self):
        Base.metadata.create_all(bind=engine)
        
    def insert_companies(self, chunksize = 100000) -> None:
        session = SessionLocal()
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
                    session.bulk_save_objects([Company(name=name) for name in new_names])
                    session.commit()
                    
        except IntegrityError:
            session.rollback()
            
        finally:
            session.close()
            
    def insert_employment_statuses(self, chunksize = 100000) -> None:
        session = SessionLocal()
        seen_employment_status_names = set()
        seen_employment_duration_names = set()

        try:
            for chunk in pd.read_csv(self.csv, usecols=['status'], chunksize=chunksize):
                chunk = chunk.dropna(subset=['status'])
                unique_status_entries = set(chunk['status'].unique())

                new_employment_status_names = set()
                new_employment_duration_names = set()

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
                        EmploymentStatus(status=status_name) for status_name in new_employment_status_names
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
          
    def insert_reviews(self, chunksize=100000) -> None:
        batch_number = 0  
        session = SessionLocal()
        
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
                            recommended=self.__safe_str(row["Recommend"]),
                            ceo_approval=self.__safe_str(row["CEO Approval"]),
                            business_outlook=self.__safe_str(row["Business Outlook"]),
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

                        review_objects.append(review)

                    except Exception as e:
                        print(f"Error on row index {idx}: {e}")

                if review_objects:
                    session.bulk_save_objects(review_objects)
                    session.commit()
                print(f"BATCH {batch_number} - PROCESSED")

        except IntegrityError as e:
            print(f"Commit failed: {e}")
            session.rollback()

        finally:
            session.close()