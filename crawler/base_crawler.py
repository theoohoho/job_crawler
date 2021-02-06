import requests
from typing import List, Optional
from bs4 import BeautifulSoup
from schema.job_event import JobEvent


class TargetSource:
    """ The data source url of target."""
    YOURATTOR = 'https://www.yourator.co/api/v2/jobs?term[]={keyword}'
    ONE_ZERO_FOUR = 'https://www.104.com.tw/jobs/search/?&jobsource=2018indexpoc&keyword={keyword}'


def crawler_exception_handler(func):
    def wrapper(self, *args, **kwargs):
        print(f'Start running {self.name} crawler...')
        result = func(self, *args, **kwargs)
        print(f'Successed web scraping job, continue return result...')
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
    def parsed_soup(self, raw_data) -> List:
        pass


class BaseCrawler(BaseParsingInterface, BaseHTMLParsingInterface):
    def __init__(self, source: TargetSource = None, **kwargs):
        self.source: str = source
        self.filter_keyword: Optional[str] = kwargs.get('filter_keyword')

        print(
            f'Setup {self.name} crawler, the filter keyword is {self.filter_keyword}')

    def __doc__():
        return """The Base crawler to support different data source."""

    def request_target_source(self) -> str:

        print(f'Send requst to the target source of {self.name} crawler...')

        source_url = self.source.format(keyword=self.filter_keyword)
        res = requests.get(source_url)
        return res.text

    def parse(self, raw_data) -> List[JobEvent]:

        print('Parsing raw data from target source...')

        parsed_result = []
        for data in raw_data:
            parsed_data = JobEvent(
                job_title=self._get_job_title(data),
                company=self._get_job_company(data),
                job_url=self._get_job_link(data),
                company_url=self._get_company_link(data),
                job_area=self._get_job_area(data),
                update_time=self._get_update_time(data)
            )
            parsed_result.append(parsed_data)
        return parsed_result

    @crawler_exception_handler
    def run(self, **kwargs) -> List[JobEvent]:
        self.filter_keyword = kwargs.get('filter_keyword')

        raw_source = self.request_target_source()
        raw_data = BeautifulSoup(raw_source, "html.parser")
        job_list = self.parsed_soup(raw_data)
        parsed_results = self.parse(job_list)

        return parsed_results

    def set_keyword(self, filter_keyword: str) -> None:
        self.filter_keyword = filter_keyword
