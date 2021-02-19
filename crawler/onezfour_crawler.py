"""
Defined the crawler to crawling target source: 104
"""
from typing import List
from crawler.base_crawler import BaseCrawler, TargetSource
import bs4.element as bs4_element


class OneZaroFourCrawler(BaseCrawler):
    """ The crawler module of 104."""
    name = '104'
    source_url: TargetSource = TargetSource.ONE_ZERO_FOUR

    def __init__(self, filter_keyword: str = None):
        """Initial 104 crawler module"""
        super().__init__(filter_keyword=filter_keyword)

    def _get_job_company(self, data: bs4_element.Tag) -> str:
        return data.get("data-cust-name")

    def _get_job_title(self, data: bs4_element.Tag) -> str:
        return data.get("data-job-name")

    def _get_job_link(self, data: bs4_element.Tag) -> str:
        return f"https:{data.find_all('a', class_='js-job-link')[0].get('href')}"

    def _get_company_link(self, data: bs4_element.Tag) -> str:
        return f"https:{data.find_all('a')[1].get('href')}"

    def _get_job_area(self, data: bs4_element.Tag) -> str:
        if data.get('data-indcat-desc'):
            return data.find_all('li')[3].text
        else:
            return data.find_all('li')[2].text

    def extract_job_list(self, soup: bs4_element.Tag) -> List:
        return soup.find_all("article")


if __name__ == '__main__':
    onezfour_crawler = OneZaroFourCrawler()
    result = onezfour_crawler.run(filter_keyword='node.js')
    print(result)
