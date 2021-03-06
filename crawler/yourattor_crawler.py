"""
Defined the crawler to crawling target source: Yourattor
"""
import json
from typing import List
from crawler.base_crawler import BaseCrawler, TargetSource
from schema.job_event import JobEvent
from utils.decorators import crawler_exception_handler


class YourattorCrawler(BaseCrawler):
    """ The crawler module of Yourattor."""
    name = 'yourattor'
    source_url: TargetSource = TargetSource.YOURATTOR

    def __init__(self, filter_keyword: str = None):
        """Initial yourattor crawler module"""
        super().__init__(filter_keyword=filter_keyword)

    def _get_job_company(self, data) -> str:
        return data['company']['brand']

    def _get_job_title(self, data) -> str:
        return data['name']

    def _get_job_area(self, data) -> str:
        return data['country_name']

    def _get_job_link(self, data) -> str:
        return f"https://www.yourator.co{data['path']}"

    def _get_company_link(self, data) -> str:
        return f"https://www.yourator.co{data['company']['path']}"

    @crawler_exception_handler
    def run(self) -> List[JobEvent]:

        source_data = self.fetch_target_source()
        job_list = json.loads(source_data)['jobs']
        job_events = self.parse_job(job_list)

        return job_events


if __name__ == '__main__':
    yourattor_crawler = YourattorCrawler()
    result = yourattor_crawler.run(filter_keyword='node.js')
    print(result)
