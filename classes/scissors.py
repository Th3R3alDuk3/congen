from re import sub, findall
from string import punctuation
from itertools import chain


punctuation += "„“‚‘«»‹›…"


class Scissors:

    strings = set()

    def __init__(self, min_string_length: int, max_string_length: int):

        self.min_string_length = min_string_length
        self.max_string_length = max_string_length

    @staticmethod
    def _prepare(text: str) -> str:

        # utf-8 encoding
        text = text.encode("utf-8", errors="ignore").decode("utf-8")
        # remove unicode whitespace characters
        text = sub(r"\s+", " ", text)

        return text.strip()

    @staticmethod
    def _extract(text: str) -> iter:

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

        for pattern in chain(*patterns):
            for subtext in findall(pattern, text):
                yield subtext.strip()

    @staticmethod
    def _sanitize(text: str) -> iter:

        text = sub(f"^[{punctuation} ]+", "", text)
        text = sub(f"[{punctuation} ]+$", "", text)

        yield text

        text = sub(f"[{punctuation}]+", "", text)

        yield text

    def _threshold(self, text: str) -> str:
        if self.min_string_length < len(text) < self.max_string_length:
            return text

    def process(self, text: str) -> iter:

        text = self._prepare(text)
        texts = {text, *self._extract(text)}

        step1 = chain(*map(lambda _: _.split(), texts))
        step2 = chain(*map(self._sanitize, {*texts, *step1}))
        step3 = map(self._threshold, step2)

        for string in set(step3):
            if string and string not in self.strings:
                self.strings.add(string)
                yield string
