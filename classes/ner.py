from sys import stderr
from bs4 import BeautifulSoup
from spacy import load
from typing import Generator, List
from collections import defaultdict


class NER:

    entities = defaultdict(set)

    def __init__(self, ner_file: str):
        self.nlp = load(ner_file)

    def recognize_entities(self, entries: Generator, labels: List[str]):
                
        for index, entry in enumerate(entries):
            
            print(f"{index} {entry.path}", file=stderr)

            item = entry.get_item()
            html = bytes(item.content)

            soup = BeautifulSoup(html, "html.parser")
            text = soup.get_text()

            doc = self.nlp(text)
            for entity in doc.ents:
                self.entities[entity.label_].add(entity.text)
