import re


class TextCleaner:

    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean extracted resume text.
        """

        text = re.sub(r"\s+", " ", text)

        text = text.strip()

        return text