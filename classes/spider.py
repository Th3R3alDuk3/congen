from scrapy import Spider, Request
from classes.parser import Parser


class Spiwix(Spider, Parser):

    name = "spiwix"

    # html tags to filter
    tags = {"h1", "h2", "h3", "h4", "a[@title]", "b", "u", "i"}

    def __init__(self, search_strings: list, languages: list, max_links: int, **kwargs):

        self.search_strings = search_strings
        self.languages = languages
        self.max_links = max_links

        # min_ and max_string_length
        super().__init__(**kwargs)

    def start_requests(self) -> iter:
        for language in self.languages:
            for search_string in self.search_strings:
                yield Request(
                    # https://wiki.kiwix.org/wiki/OPDS
                    "http://localhost/catalog/search?tag=wikipedia&lang={}&pattern={}".format(
                        language,
                        search_string
                    ), callback=self.parse_catalogs
                )

    def parse_catalogs(self, response, page_links: int = 50) -> iter:

        # remove all namespaces for better handling
        response.selector.remove_namespaces()

        for href in response.xpath("//entry/link[@type='text/html']/@href").getall():
            for search_string in self.search_strings:
                # scroll through several pages of a certain length until the maximum is reached
                for i in range(0, self.max_links, min(page_links, self.max_links)):
                    yield Request(
                        "http://localhost/search?content={}&start={}&pageLength={}&pattern={}".format(
                            href.strip("/"),
                            i + 1, min(i + page_links, self.max_links),
                            search_string
                        ), callback=self.parse_results
                    )

    def parse_results(self, response) -> iter:
        for href in response.xpath("//div[@class='results']//a/@href").getall():
            yield Request(
                "http://localhost/{}".format(
                    href.strip('/')
                ), callback=self.parse
            )

    def parse(self, response, **kwargs):
        for div in response.xpath("//div[@id='content']"):
            for tag in self.tags:
                for text in div.xpath(f"//{tag}/text()").getall():
                    if text:
                        for string in self.process(text):
                            print(string)
