import re
import string
import itertools


string.punctuation += "„“‚‘«»‹›"


class Analyzer:

    strings = set()

    def __init__(self, min_string_length: int = 3, max_string_length: int = 30):

        self.min_string_length = min_string_length
        self.max_string_length = max_string_length

    @staticmethod
    def prepare(text: str) -> str:

        # utf-8 encoding
        text = text.encode("utf-8", errors="ignore").decode("utf-8")
        # remove unicode whitespace characters
        text = re.sub(r"\s+", " ", text)

        return text.strip()

    @staticmethod
    def extract(text: str) -> iter:

        yield text

        patterns = [
            # brackets
            {r"\((.*)\)", r"\{(.*)\}", r"\[(.*)\]"},
            # quotation marks
            {r'"(.*)"', r"'(.*)'", r"´(.*)´", r"`(.*)`"},
            # deu, eng and fra quotation marks
            {r"„(.*)“", r"‚(.*)‘"},
            {r"“(.*)”", r"‘(.*)’"},
            {r"«(.*)»", r"‹(.*)›"}
        ]

        for pattern in itertools.chain(*patterns):
            for subtext in re.findall(pattern, text):
                yield subtext.strip()

    @staticmethod
    def split(text: str) -> iter:

        yield text

        for subtext in text.split():
            yield subtext

    @staticmethod
    def sanitize(text: str) -> iter:

        text = re.sub(f"^[{string.punctuation} ]+", "", text)
        text = re.sub(f"[{string.punctuation} ]+$", "", text)

        yield text

        text = re.sub(f"[{string.punctuation}]+", "", text)

        yield text

    def threshold(self, text: str) -> str:
        if self.min_string_length < len(text) < self.max_string_length:
            return text

    def process(self, text: str):

        text = self.prepare(text)

        for _text in self.extract(text):
            for __text in self.split(_text):
                for ___text in self.sanitize(__text):

                    ___text = self.threshold(___text)

                    if ___text and ___text not in self.strings:
                        self.strings.add(___text)
                        # yield ("prepare", text), ("extract", _text), ("split", __text), ("sanitize", ___text)
                        yield ___text
