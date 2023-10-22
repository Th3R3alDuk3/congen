#!/usr/bin/python3

import argparse
from classes.ner import NER
from classes.zim import ZIM


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("search_strings", nargs="+")
    parser.add_argument("-l", "--languages", nargs="+", help="ISO-639-3")
    parser.add_argument("--max_links", type=int, default=300)
    parser.add_argument("--min_string_length", type=int, default=3)
    parser.add_argument("--max_string_length", type=int, default=20)

    args = parser.parse_args()
    
    #

    zim = ZIM("wikipedia/wikipedia_en_all_nopic_2023-09.zim")    
    entries = zim.search_entries(args.search_strings)

    #
    
    ner = NER("en_core_web_sm")
    ner.recognize_entities(entries, ["PERSON"])


if __name__ == "__main__":
    main()
