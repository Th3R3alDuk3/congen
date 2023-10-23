from bs4 import BeautifulSoup
from spacy import load
from spacy.tokens import Doc


class NER:

    _nlp = None

    @classmethod
    def load(cls, nlp_path: str):
        cls._nlp = load(nlp_path)

    @classmethod
    def predict(cls, content: bytes) -> Doc:

        assert cls._nlp
        
        soup = BeautifulSoup(content, "html.parser")
        text = soup.get_text(separator=" ", strip=True)

        return cls._nlp(text)
