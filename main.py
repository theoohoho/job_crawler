from crawler import yourattor_crawler, onezfour_crawler
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run Job crawler.')
    parser.add_argument('--yourattor', help='select yourattor as target source', action='store_true')
    parser.add_argument('--onezfour', help='select 104 as target source', action='store_true')
    parser.add_argument('--all', help='select all target source', action='store_true')
    parser.add_argument('--keyword', metavar='search target', type=str, nargs='+',help='an filter keyword for crawling')
    parser.set_defaults(all=True)
    args = parser.parse_args()
    if args.yourattor:
        keyword = ''.join(args.keyword)
        print(yourattor_crawler.YourattorCrawler(filter_keyword=keyword).run())
    elif args.onezfour:
        keyword = ''.join(args.keyword)
        print(onezfour_crawler.OneZaroFourCrawler(filter_keyword=keyword).run())