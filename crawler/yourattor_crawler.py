"""
The crawler of Yourattor
"""
import requests
import json
from pydantic import BaseModel
from typing import List
from crawler.base_crawler import BaseCrawler, TargetSource, crawler_exception_handler


class YourattorCrawler(BaseCrawler):
    """ The crawler of Yourattor."""
    name = 'yourattor'

    def __init__(self, filter_keyword: str = None):
        super().__init__(source=TargetSource.YOURATTOR, filter_keyword=filter_keyword)

    def _get_job_company(self, data) -> str:
        return data['company']['brand']

    def _get_job_title(self, data) -> str:
        return data['name']

    def _get_job_area(self, data) -> str:
        return data['country_name']

    def _get_job_link(self, data) -> str:
        return self.source + data['path']

    @crawler_exception_handler
    def run(self, **kwargs) -> None:
        self.filter_keyword = kwargs.get('filter_keyword')

        target_raw_source = self.request_target_source()
        target_json_source = json.loads(target_raw_source)
        parsed_results = self.parse(target_json_source['jobs'])

        return parsed_results


if __name__ == '__main__':
    yourattor_crawler = YourattorCrawler()
    result = yourattor_crawler.run(filter_keyword='node.js')
    print(result)
