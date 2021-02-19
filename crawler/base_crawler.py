"""Defined a base crawler module"""

import requests

from typing import List, Optional
from bs4 import BeautifulSoup, element as bs4_element
from schema.job_event import JobEvent

from enum import Enum


class TargetSource(Enum):
    """ The data source url of target."""
    YOURATTOR = 'https://www.yourator.co/api/v2/jobs?term[]={keyword}'
    ONE_ZERO_FOUR = 'https://www.104.com.tw/jobs/search/?&jobsource=2018indexpoc&keyword={keyword}'


def crawler_exception_handler(func):
    def wrapper(self, *args, **kwargs):
        print(f'Start running {self.name} crawler...')
        result = func(self, *args, **kwargs)
        print('Successed web scraping job, continue return result...')
        return result
    return wrapper


class BaseParsingInterface:
    """ Base parsing method interface."""

    def _get_job_company(self, data) -> str:
        pass

    def _get_job_title(self, data) -> str:
        pass

    def _get_job_area(self, data) -> str:
        pass

    def _get_job_desc(self, data) -> str:
        pass

    def _get_job_link(self, data) -> str:
        pass

    def _get_company_link(self, data) -> str:
        pass

    def _get_update_time(self, data) -> str:
        pass


class BaseHTMLParsingInterface:
    def extract_job_list(self, soup: bs4_element.Tag) -> List:
        """Extract job list from soap object

        Args:
            soup (bs4_element.Tag): a soap data that parsed by BeautifulSoap

        Returns:
            List: a job list that extract from soap object
        """
        pass


class BaseCrawler(BaseParsingInterface, BaseHTMLParsingInterface):
    """The Base crawler to support different data source."""
    source_url: TargetSource = ''

    def __init__(self, **kwargs):
        """Initial base crawler module."""
        self.filter_keyword: Optional[str] = kwargs.get('filter_keyword')

        print(
            f'Setup {self.name} crawler, the filter keyword is {self.filter_keyword}')

    def fetch_target_source(self) -> str:
        """Fetch source text from target source url"""
        print(f'Send requst to the target source of {self.name} crawler...')

        source_url = self.source_url.format(keyword=self.filter_keyword)
        res = requests.get(source_url)
        return res.text

    def parse_job(self, job_list: List) -> List[JobEvent]:
        """Parse job list and Package a list of data job event data format

        Args:
            job_list (List): a job list that 

        Returns:
            List[JobEvent]: [description]
        """
        print('Parsing job data from job list...')

        parsed_result = []
        for job_data in job_list:
            job_event = JobEvent(
                job_title=self._get_job_title(job_data),
                company=self._get_job_company(job_data),
                job_url=self._get_job_link(job_data),
                company_url=self._get_company_link(job_data),
                job_area=self._get_job_area(job_data),
                update_time=self._get_update_time(job_data)
            )
            parsed_result.append(job_event)
        return parsed_result

    @crawler_exception_handler
    def run(self, **kwargs) -> List[JobEvent]:
        """Running crawler job to scraping target source

        Returns:
            List[JobEvent]: a list of job event
        """
        self.filter_keyword = kwargs.get('filter_keyword')

        source_data = self.fetch_target_source()
        soup = BeautifulSoup(source_data, "html.parser")
        job_list = self.extract_job_list(soup)
        job_events = self.parse_job(job_list)

        return job_events

    def set_keyword(self, filter_keyword: str) -> None:
        self.filter_keyword = filter_keyword
