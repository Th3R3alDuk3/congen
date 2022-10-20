#!/usr/bin/python3

import argparse
from scrapy.crawler import CrawlerProcess
from classes.spider import Spiwix


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("search_strings", nargs="+")
    parser.add_argument("-l", "--languages", nargs="+", help="ISO-639-3")
    parser.add_argument("--max_links", type=int, default=300)
    parser.add_argument("--min_string_length", type=int, default=3)
    parser.add_argument("--max_string_length", type=int, default=20)

    args = parser.parse_args()

    process = CrawlerProcess()
    # TODO: require -> search_strings, languages, max_pages, min_string_length, max_string_length
    process.crawl(Spiwix, **vars(args))
    process.start()


if __name__ == "__main__":
    main()
