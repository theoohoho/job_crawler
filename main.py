"""The entry point to execute job_crawler
"""

import argparse
import time

from crawler import yourattor_crawler, onezfour_crawler
from worker import Worker


def worker_runner(args: argparse.Namespace, keyword: str) -> Worker:
    """Setup worker runner

    Args:
        args (argparse.Namespace): a object contain arguments of command
        keyword (str): a keyword let crawler to filter result

    Returns:
        Worker: Worker class
    """
    try:
        setup_crawler = []
        worker = Worker()
        yourator = yourattor_crawler.YourattorCrawler(filter_keyword=keyword)
        onezfour = onezfour_crawler.OneZaroFourCrawler(filter_keyword=keyword)
        if args.yourattor:
            setup_crawler.append(yourator)
        elif args.onezfour:
            setup_crawler.append(onezfour)
        elif args.all:
            setup_crawler.extend([yourator, onezfour])

        worker.setup_crawler(setup_crawler)
        return worker
    except Exception:
        raise


def main(args: argparse.Namespace) -> None:
    """Setup and execute worker_runner

    Args:
        args (argparse.Namespace): a object contain arguments of command
    """
    try:
        keyword = ''.join(args.keyword)
        worker = worker_runner(args, keyword)
        while True:
            if args.enable_db:
                worker.run_crawler_in_db()
            else:
                res = worker.run_crawler()
                print('Crawler result:\n')
                print(res)
            if not args.interval:
                break
            time.sleep(args.interval)
    except Exception:
        raise


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run Job crawler.')
    parser.add_argument('-k', '--keyword', metavar='keyword to search',
                        type=str, help='an filter keyword for crawling', required=True)
    parser.add_argument('-i', '--interval', metavar='seconds',
                        type=int, help='set interval running time', default=0)
    parser.add_argument('-a', '--all', help='select all target source', action='store_true', default=True)
    parser.add_argument('--yourattor', help='select yourattor as target source', action='store_true')
    parser.add_argument('--onezfour', help='select 104 as target source', action='store_true')
    parser.add_argument('--enable_db', help='enable save in database', action='store_true')

    args = parser.parse_args()
    main(args)
