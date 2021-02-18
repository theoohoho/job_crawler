"""
Worker runner can accept different crawler to scraping
"""
from typing import List

from sqlalchemy.exc import InvalidRequestError

from utils.exception import WorkerRunningError, WorkerSetupCrawlerFail

from schema.job_event import JobEvent as JobEventSchema
from crud.crud_job_event import job_event
from crawler.base_crawler import BaseCrawler


def save_database(func):
    def wrapper(*args, **kwargs):
        from database.database_session import get_db_session
        try:
            with get_db_session() as db_session:
                raw_data = func(*args, **kwargs)
                print('Ready to save scraping data into database')
                job_event.add_all(db_session, raw_data)
                db_session.commit()
            print('Successed saving data into database')
        except InvalidRequestError:
            raise
        except Exception:
            raise
    return wrapper


def exception_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except WorkerRunningError:
            raise
        except WorkerSetupCrawlerFail:
            raise
        except Exception:
            raise
    return wrapper


class Worker():
    def __init__(self) -> None:
        self.tasks: List[BaseCrawler] = []
        self.result_data = []

    @exception_handler
    def add_crawler(self, crawler: BaseCrawler) -> None:
        self.tasks.append(crawler)

    @exception_handler
    def setup_crawler(self, crawlers: List[BaseCrawler]) -> None:
        self.tasks.extend(crawlers)

    @exception_handler
    def run_crawler(self) -> List[JobEventSchema]:

        print(f"Ready for scraping, current task: {self.tasks}")

        crawler_raw_data = []
        for task in self.tasks:
            res = task.run()
            crawler_raw_data.extend(res)
        return crawler_raw_data

    @save_database
    def run_crawler_in_db(self) -> List[JobEventSchema]:
        return self.run_crawler()
