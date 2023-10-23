#!/usr/bin/python3

from os import cpu_count
from argparse import ArgumentParser
from configparser import ConfigParser
from concurrent.futures import ProcessPoolExecutor
from classes.zim import ZIM
from classes.ner import NER


BLACKLIST_TEXT = set()


def main():

    arg_parser = ArgumentParser()
    arg_parser.add_argument("language", help="ISO-639-2")
    arg_parser.add_argument("search_strings", nargs="+")

    args = arg_parser.parse_args()
    
    #

    cfg_parser = ConfigParser()
    cfg_parser.read("languages.cfg")

    #

    zim_file = cfg_parser.get(args.language, "zim_file")
    zim = ZIM(zim_file)

    ner_path = cfg_parser.get(args.language, "ner_path")
    NER.load(ner_path)

    for search_string in args.search_strings:

        items = zim.suggest(search_string)

        whitelist = dict()
        for item in items:
            whitelist[item.path] = bytes(item.content)

        with ProcessPoolExecutor(cpu_count()) as pool:
            for document in pool.map(NER.predict, whitelist.values()):
                
                for token in document:
                    if token.pos_ in {'NOUN', 'PROPN', 'VERB', 'ADJ', 'NUM'}:
                        if token.text not in BLACKLIST_TEXT:    

                            BLACKLIST_TEXT.add(token.text)                        
                            print(token.text)

                for entity in document.ents:
                    if entity.label_ in {'WORK_OF_ART', 'GPE', 'ORG', 'PERSON', 'EVENT', 'FAC', 'PRODUCT', 'LAW', 'NORP', 'LOC'}:
                        if entity.text not in BLACKLIST_TEXT:

                            BLACKLIST_TEXT.add(entity.text)
                            print(entity.text)


if __name__ == "__main__":
    main()
