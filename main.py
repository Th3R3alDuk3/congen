#!/usr/bin/python3

import logging
import argparse
from scrapy.crawler import CrawlerProcess
from classes.spider import Spider


def main():

    logging.getLogger("scrapy").propagate = False

    parser = argparse.ArgumentParser()
    parser.add_argument("search_words", nargs="+")
    parser.add_argument("-l", "--languages", nargs="+", help="ISO-639-2/T")

    args = parser.parse_args()

    process = CrawlerProcess()
    process.crawl(Spider, **vars(args))
    process.start()


if __name__ == "__main__":
    main()
