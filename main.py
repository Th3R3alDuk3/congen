#!/usr/bin/python3

import argparse
from scrapy.crawler import CrawlerProcess
from classes.spider import Spider


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("search_words", nargs="+")
    parser.add_argument("-l", "--languages", nargs="+", help="ISO-639-3")

    args = parser.parse_args()

    process = CrawlerProcess()
    process.crawl(Spider, **vars(args))
    process.start()


if __name__ == "__main__":
    main()
