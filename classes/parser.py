from re import sub, findall
from itertools import chain
from string import punctuation
punctuation += "„“‚‘«»‹›…"


class Parser:

    strings = set()

    def __init__(self, min_string_length: int, max_string_length: int):

        self.min_string_length = min_string_length
        self.max_string_length = max_string_length

    @staticmethod
    def _prepare(string: str) -> str:

        # utf-8 encoding
        string = string.encode("utf-8", errors="ignore").decode("utf-8")
        # remove unicode whitespace characters
        string = sub(r"\s+", " ", string)

        return string.strip()

    @staticmethod
    def _extract(string: str) -> set:

        strings = {
            string,
            string.replace(" ", ""),
            sub(f"[{punctuation} ]+", "", string),
            sub(f"[{punctuation}]+", "", string),
            *string.split()
        }

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
            for substring in findall(pattern, string):
                strings.add(substring.strip())

        return strings

    def _filter(self, string: str) -> bool:

        if string in self.strings:
            return False

        if string.isdigit():
            return False

        if len(string) < self.min_string_length:
            return False
        if len(string) > self.max_string_length:
            return False

        self.strings.add(string)

        return True

    @staticmethod
    def _strip(string: str) -> str:

        string = sub(f"^[{punctuation} ]+", "", string)
        string = sub(f"[{punctuation} ]+$", "", string)

        return string

    def process(self, string: str) -> iter:

        string = self._prepare(string)

        if string:
            for substring in self._extract(string):
                if self._filter(substring):
                    yield self._strip(substring)
