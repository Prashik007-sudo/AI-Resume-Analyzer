import os

from dotenv import load_dotenv
from google import genai

from app.ai.prompts import RESUME_EXTRACTION_PROMPT

load_dotenv()


class GeminiService:

    client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY")
    )

    @staticmethod
    def extract_resume_information(text: str):

        MODEL_NAME = os.getenv("GEMINI_MODEL")

        prompt = RESUME_EXTRACTION_PROMPT.format(
            text=text
        )

        response = GeminiService.client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        from app.ai.response_parser import ResponseParser
        parsed_response = ResponseParser.parse(response.text)

        return parsed_response