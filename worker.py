"""
Worker runner can accept different crawler to scraping
"""
from typing import List

from sqlalchemy.exc import InvalidRequestError

from utils.exceptions import WorkerRunningError, WorkerSetupCrawlerFail

from schema.job_event import JobEvent as JobEventSchema
from crud.crud_job_event import job_event
from crawler.base_crawler import BaseCrawler
from utils.decorators import worker_exception_handler


def save_database(func):
    """A decorator to support worker to save job data into database
    """
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


class Worker():
    """Worker runner to setup multiple crawler job and batch running crawler job
    """

    def __init__(self) -> None:
        self.tasks: List[BaseCrawler] = []

    @worker_exception_handler
    def add_crawler(self, crawler: BaseCrawler) -> None:
        """Append crawler task into tasks list

        Args:
            crawler (BaseCrawler): a crawler for worker to execute
        """
        self.tasks.append(crawler)

    @worker_exception_handler
    def setup_crawler(self, crawlers: List[BaseCrawler]) -> None:
        """Set up crawler task into worker

        Args:
            crawlers (List[BaseCrawler]): multiple crawlers for worker to execute
        """
        self.tasks.extend(crawlers)

    @worker_exception_handler
    def run_crawler(self) -> List[JobEventSchema]:
        """Extract crawler from job list and execute it each

        Returns:
            List[JobEventSchema]: the result of crawler output
        """
        print(f"Ready for scraping, current task: {self.tasks}")

        crawling_result = []
        for task in self.tasks:
            result = task.run()
            crawling_result.extend(result)
        return crawling_result

    @save_database
    def run_crawler_in_db(self) -> List[JobEventSchema]:
        """Extract crawler from job list and execute it each. then store output into database

        Returns:
            List[JobEventSchema]: the result of crawler output
        """
        return self.run_crawler()
