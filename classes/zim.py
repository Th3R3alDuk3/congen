from sys import stderr
from typing import Generator, List
from libzim.reader import Archive
from libzim.suggestion import SuggestionSearcher


class ZIM:

    # https://libzim.readthedocs.io/en/latest/usage.html
    blacklist = set()

    def __init__(self, zim_file: str):
        self.zim = Archive(zim_file)

    def search_entries(self, search_strings: List[str]) -> Generator:

        suggestion_searcher = SuggestionSearcher(self.zim)
            
        for search_string in search_strings:

            suggestion = suggestion_searcher.suggest(search_string)
            suggestion_count = suggestion.getEstimatedMatches()
            print(f"found {suggestion_count} matches for '{search_string}'", file=stderr)

            for path in suggestion.getResults(0, suggestion_count):

                entry = self.zim.get_entry_by_path(path)

                if entry.is_redirect:
                    entry = entry.get_redirect_entry()

                if entry.path in self.blacklist:
                    continue
                
                self.blacklist.add(entry.path)
                yield entry