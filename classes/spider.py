import scrapy as scrapy

from classes.analyzer import Analyzer


class Spider(scrapy.Spider):

    name = "spiki"

    def __init__(self, languages: list, search_words: list):

        self.languages = languages
        self.search_words = search_words

    def start_requests(self) -> iter:
        for language in self.languages:
            for search_word in self.search_words:
                yield scrapy.Request(
                    # https://wiki.kiwix.org/wiki/OPDS
                    f"http://localhost/catalog/search?tag=wikipedia&lang={language}&pattern={search_word}",
                    callback=self.parse_catalogs
                )

    def parse_catalogs(self, response) -> iter:

        response.selector.remove_namespaces()

        for href in response.xpath("//entry/link[@type='text/html']/@href").getall():
            for search_word in self.search_words:
                yield scrapy.Request(
                    f"http://localhost/search?content={href.strip('/')}&pattern={search_word}",
                    callback=self.parse_results
                )

    def parse_results(self, response) -> iter:
        for href in response.xpath("//div[@class='results']//a/@href").getall():
            yield scrapy.Request(
                f"http://localhost/{href.strip('/')}",
                callback=self.parse
            )

    def parse(self, response, **kwargs):
        for div in response.xpath("//div[@id='content']"):
            for tag in {"h1", "h2", "h3", "h4", "a", "b", "u", "i"}:
                for text in div.xpath(f"//{tag}/text()").getall():
                    if text:
                        for string in Analyzer().process(text):
                            print(string)
