from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class JobEvent(BaseModel):
    """ Job event data format"""
    job_title: str = Field(..., title="", description="")
    company: str = Field(..., title="", description="")
    job_area: Optional[str] = Field(None, title="", description="")
    job_url: str = Field(..., title="", description="")
    company_url: Optional[str] = Field(None, title="", description="")
    update_time: Optional[str] = Field(None, title="", description="")
