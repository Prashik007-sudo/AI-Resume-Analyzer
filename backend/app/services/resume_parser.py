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

    @staticmethod
    def extract_linkedin(text: str):

        pattern = r"(https?://(?:www\.)?linkedin\.com/in/[^\s]+)"
    
        match = re.search(pattern, text, re.IGNORECASE)
    
        if match:
            return match.group(1).strip()
    
        return None

    @staticmethod
    def extract_github(text: str):
    
        pattern = r"(https?://(?:www\.)?github\.com/[^\s]+)"
    
        match = re.search(pattern, text, re.IGNORECASE)
    
        if match:
            return match.group(1).strip()
    
        return None

    @staticmethod
    def extract_portfolio(text: str):
    
        patterns = [
    
            r"(https?://(?:www\.)?[^\s]+\.(?:com|dev|io|app|me|tech|xyz|site|online)[^\s]*)",
    
        ]
    
        for pattern in patterns:
    
            matches = re.findall(pattern, text, re.IGNORECASE)
    
            for url in matches:
    
                if (
                    "linkedin.com" not in url.lower()
                    and "github.com" not in url.lower()
                ):
                    return url.strip()
    
        return None