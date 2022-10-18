import logging
from scrapy.crawler import CrawlerProcess
from classes.spider import Spider


def main():

    logging.getLogger('scrapy').propagate = False

    process = CrawlerProcess()
    process.crawl(Spider, languages=["deu"], search_words=["Harry Potter"])
    process.start()


if __name__ == "__main__":
    main()
