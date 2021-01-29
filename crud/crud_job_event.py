"""A crud method of job_event"""
from crud.crud_base import CRUDBase
from model.job_event import JobEvent
from schema.job_event import JobEvent as JobEventSchema


class CRUDJobEvent(CRUDBase[JobEvent, JobEventSchema]):
    """Defined job_event crud method"""
    pass


job_event = CRUDJobEvent(JobEvent)
