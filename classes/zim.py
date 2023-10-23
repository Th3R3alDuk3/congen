from sys import stderr
from typing import Iterable
from libzim import Item
from libzim.reader import Archive
from libzim.suggestion import SuggestionSearcher


class ZIM:

    # https://libzim.readthedocs.io/en/latest/usage.html

    def __init__(self, zim_file: str):

        self.archive = Archive(zim_file)

        # look up in suggestion database
        self.searcher = SuggestionSearcher(self.archive)

    def suggest(self, search_string: str) -> Iterable[Item]:
            
        suggestion = self.searcher.suggest(search_string)
        suggestion_count = suggestion.getEstimatedMatches()
        print(f"found {suggestion_count} matches for '{search_string}'", file=stderr)

        for path in suggestion.getResults(0, suggestion_count):

            entry = self.archive.get_entry_by_path(path)
            # follow redirects is is_redirect is true
            yield entry.get_item()