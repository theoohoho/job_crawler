import requests
import json
from pydantic import BaseModel
from typing import List
from .base_crawler import BaseCrawler, TargetSource

class ParsedData(BaseModel):
    """ Paesed data format"""
    title: str
    company: str
    country: str
    url: str


class YourattorCrawler(BaseCrawler):
    """ The crawler of Yourattor."""
    name = 'yourattor'

    def __init__(self, filter_keyword: str = None):
        super().__init__(source=TargetSource.YOURATTOR, filter_keyword=filter_keyword)

    def _get_job_company(self, data) -> str:
        return data['company']['brand']

    def _get_job_title(self, data) -> str:
        return data['name']

    def _get_job_country(self, data) -> str:
        return data['country_name']

    def _get_job_link(self, data) -> str:
        return self.source + data['path']

    def parse(self, raw_data: dict) -> List[ParsedData]:
        parsed_result = []
        for data in raw_data:
            parsed_result.append({
                "title": self._get_job_title(data),
                "company": self._get_job_company(data),
                "country": self._get_job_country(data),
                "url": self._get_job_link(data)
            })
        return parsed_result

    def extract_target_resoure(self):
        return self.request_target_source(
            f"{self.source}/api/v2/jobs?=python", {
                'page': 1,
                'term[]': self.filter_keyword
            })

    def run(self, filter_keyword: str = None) -> None:
        if filter_keyword:
            self.filter_keyword = filter_keyword

        raw_data = self.extract_target_resoure()
        raw_data = json.loads(raw_data)
        parsed_results = self.parse(raw_data['jobs'])
        return parsed_results


if __name__ == '__main__':
    yourattor_crawler = YourattorCrawler()
    yourattor_crawler.run(filter_keyword='node.js')
