"""
Defined the crawler to crawling target source: Yourattor
"""
import json
from typing import List
from crawler.base_crawler import BaseCrawler, TargetSource, crawler_exception_handler
from schema.job_event import JobEvent


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
        return self.source_url + data['path']

    @crawler_exception_handler
    def run(self, **kwargs) -> List[JobEvent]:
        self.filter_keyword = kwargs.get('filter_keyword')

        source_data = self.fetch_target_source()
        job_list = json.loads(source_data)['jobs']
        job_events = self.parse_job(job_list)

        return job_events


if __name__ == '__main__':
    yourattor_crawler = YourattorCrawler()
    result = yourattor_crawler.run(filter_keyword='node.js')
    print(result)
