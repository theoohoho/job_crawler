from pydantic import BaseModel
from typing import Optional


class ParsedData(BaseModel):
    """ Paesed data format"""
    job_title: str
    company: str
    job_area: Optional[str]
    job_desc: Optional[str]
    job_url: str
    company_url: Optional[str]
    update_time: Optional[str]
