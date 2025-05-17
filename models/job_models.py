from typing import List
from pydantic import BaseModel, Field

class JobDocument(BaseModel):
    title: str = Field(..., description="The title of the job position (e.g., 'Software Engineer', 'Marketing Manager').")
    summary: str = Field(..., description="A brief summary or overview of the job, highlighting its purpose and key objectives.")
    company: str = Field(..., description="The name of the company or organization offering the job.")
    location: str = Field(..., description="The geographic location of the job (e.g., city, country, or remote).")
    responsibilities: List[str] = Field(..., description="A list of duties and tasks the candidate is expected to perform in this role.")
    requirements: List[str] = Field(..., description="A list of qualifications, skills, or experience required or preferred for the job.")
