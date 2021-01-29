from sqlalchemy import Column, Integer, String, DateTime
from database.base_class import Base


class JobEvent(Base):
    __tablename__ = "job_event"

    id = Column(Integer, primary_key=True, index=True)
    job_title = Column(String)
    company = Column(String)
    job_area = Column(String)
    job_url = Column(String)
    company_url = Column(String)
    update_time = Column(String, server_default=None)
