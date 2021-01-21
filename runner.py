from crawler.base_crawler import BaseCrawler
from crawler.yourattor_crawler import YourattorCrawler
from crawler.onezfour_crawler import OneZaroFourCrawler
from typing import List

class Worker():
    def __init__(self):
        self.tasks: List[BaseCrawler] = []

    def add_crawler(self, crawler: BaseCrawler):
        self.tasks.append(crawler)

    def run(self):
        for task in self.tasks:
            task.run()

if __name__ == '__main__':
    worker = Worker()
    worker.add_crawler(YourattorCrawler(filter_keyword='python'))
    # worker.add(OneZaroFourCrawler(filter_keyword='python'))
    while True:
        worker.run()
        time.sleep(20)
