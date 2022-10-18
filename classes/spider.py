import scrapy as scrapy


class Spider(scrapy.Spider):

    # https://wiki.kiwix.org/wiki/OPDS

    name = "spiki"

    def __init__(self, languages: list, search_words: list):

        self.languages = languages
        self.search_words = search_words

    def start_requests(self) -> iter:
        for language in self.languages:
            yield scrapy.Request(
                f"http://localhost/catalog/search?tag=wikipedia&lang={language}",
                callback=self.parse_catalogs
            )

    def parse_catalogs(self, response) -> iter:

        response.selector.remove_namespaces()

        for href in response.xpath("//entry/link[@type='text/html']/@href").extract():
            for search_word in self.search_words:
                yield scrapy.Request(
                    f"http://localhost/search?content={href[1:]}&pattern={search_word}",
                    callback=self.parse_results
                )

    def parse_results(self, response) -> iter:
        for href in response.xpath("//div[@class='results']//a/@href").extract():
            yield scrapy.Request(
                f"http://localhost{href}",
                callback=self.parse
            )

    def parse(self, response, **kwargs):
        for div in response.xpath("//div[@id='content']"):
            for tag in {"h1", "h2", "h3", "h4", "a", "b", "u", "i"}:
                for text in div.xpath(f"//{tag}/text()").extract():
                    if text:
                        print(text.strip())
