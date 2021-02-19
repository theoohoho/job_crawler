"""Definition decorator
"""

from utils.exceptions import WorkerRunningError, WorkerSetupCrawlerFail


def crawler_exception_handler(func):
    """A decorator to handle exception from crawler
    """
    def wrapper(self, *args, **kwargs):
        try:
            print(f'Start running {self.name} crawler...')
            result = func(self, *args, **kwargs)
            print('Successed web scraping job, continue return result...')
            return result
        except Exception:
            raise
    return wrapper


def worker_exception_handler(func):
    """A decorator to handle exception from worker
    """
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


def crud_exception_handler(func):
    """A decorator to handle exception from db crud operation
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            raise
    return wrapper
