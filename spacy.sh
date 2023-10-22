#!/usr/bin/bash

languages="de en fr"

for language in $languages; do
    python3 -m spacy download ${language}
done

