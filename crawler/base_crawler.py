import requests
from typing import Union, List


class TargetSource:
    """ The data source url of target."""
    YOURATTOR = 'https://www.yourator.co'


class BaseParsingInterface:
    """ Base parsing method interface."""
    def run(self) -> None:
        pass

    def set_keyword(self, filter_keyword: str) -> None:
        pass

    def parse(self) -> str:
        pass

    def _get_job_company(self, data) -> str:
        pass

    def _get_job_title(self, data) -> str:
        pass

    def _get_job_country(self, data) -> str:
        pass

    def _get_job_desc(self, data) -> str:
        pass

    def _get_job_link(self, data) -> str:
        pass


class BaseCrawler(BaseParsingInterface):
    def __init__(self, source: TargetSource = None, filter_keyword: str = None):
        self.source = source
        self.filter_keyword = filter_keyword

    def __doc__():
        return """The Base crawler to support different data source."""

    def request_target_source(self, source_url: str = None, params=None) -> str:
        r = requests.get(source_url, params)
        return r.text

    def run(self) -> None:
        pass

    def set_keyword(self, filter_keyword: str) -> None:
        self.filter_keyword = filter_keyword
