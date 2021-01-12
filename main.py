from .crawler.yourattor_crawler import YourattorCrawler
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run Job crawler.')
    parser.add_argument('--keyword', metavar='search target', type=str, nargs='+',help='an filter keyword for crawling')
    args = parser.parse_args()
    keyword = ''.join(args.keyword)
    print(YourattorCrawler(filter_keyword=keyword).run())
