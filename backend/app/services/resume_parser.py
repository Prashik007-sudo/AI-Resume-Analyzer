import re


class ResumeParser:

    @staticmethod
    def extract_email(text: str):

        pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"

        match = re.search(pattern, text)

        if match:
            return match.group()

        return None