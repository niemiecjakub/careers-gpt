from typing import List, Optional
from pydantic import BaseModel, Field


class Link(BaseModel):
    name: str = Field(..., description="The name or label for the link, such as 'LinkedIn', 'GitHub', or 'Portfolio'.")
    url: str = Field(..., description="The URL or web address that the link points to.")


class PersonalDetails(BaseModel):
    name: str = Field(..., description="Full name of the individual.")
    phone: str = Field(..., description="Primary phone number for contact.")
    email: str = Field(..., description="Primary email address for correspondence.")
    location: str = Field(..., description="City, region, or country of residence.")
    links: List[Link] = Field(..., description="A collection of labeled links such as LinkedIn, GitHub, portfolio, or personal website.")


class Education(BaseModel):
    degree: str = Field(..., description="The academic degree obtained.")
    institution: str = Field(..., description="The name of the educational institution.")
    location: str = Field(..., description="The geographic location of the institution (city, country).")
    description: Optional[str] = Field(None, description="Optional description of the educational experience.")
    field_of_study: str = Field(..., description="The major or field of study.")
    begin_date: Optional[str] = Field(None, description="The start date of the education period.")
    end_date: Optional[str] = Field(None, description="The end date of the education period, if applicable.")


class WorkExperience(BaseModel):
    job_title: str = Field(..., description="The job title or position held by the individual.")
    description: Optional[str] = Field(None, description="Optional summary or narrative of the role.")
    company: str = Field(..., description="The name of the company or organization.")
    location: str = Field(..., description="The geographic location of the job (city and country).")
    begin_date: Optional[str] = Field(None, description="The start date of the work period.")
    end_date: Optional[str] = Field(None, description="The end date of the work period, if applicable.")
    responsibilities: List[str] = Field(..., description="List of key duties, achievements, or responsibilities.")


class OtherSection(BaseModel):
    title: str = Field(..., description="The title of the custom section (e.g., 'Certifications', 'Projects').")
    description: Optional[str] = Field(None, description="Short summary of the section's context or purpose.")
    details: List[str] = Field(..., description="List of bullet points or descriptive items.")


class CoreCvDocument(BaseModel):
    about_me: Optional[str] = Field(None, description="A brief personal summary or professional introduction.")
    education: List[Education] = Field(default_factory=list, description="List of educational background entries.")
    work_experience: List[WorkExperience] = Field(default_factory=list, description="List of past job experiences.")
    skills: List[str] = Field(default_factory=list, description="Key technical or soft skills.")
    languages: List[str] = Field(default_factory=list, description="Languages spoken and level of proficiency.")
    other_sections: List[OtherSection] = Field(default_factory=list, description="Custom sections like certifications or hobbies.")


class CvDocument(CoreCvDocument):
    personal_details: PersonalDetails = Field(..., description="Basic personal information including name and contact details.")
