import re
import spacy

nlp = spacy.load("en_core_web_sm")


class ResumeParser:

    @staticmethod
    def extract_email(text: str):

        pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"

        match = re.search(pattern, text)

        if match:
            return match.group()

        return None
    
    @staticmethod
    def extract_phone(text: str):

        pattern = r"(?:\+91[-\s]?)?[6-9]\d{9}"

        match = re.search(pattern, text)

        if match:
          return match.group()

        return None