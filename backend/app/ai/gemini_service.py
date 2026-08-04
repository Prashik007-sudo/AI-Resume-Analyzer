import os
import logging

from dotenv import load_dotenv
from fastapi import HTTPException
from google import genai

from app.ai.prompts.resume_prompt import (
    RESUME_EXTRACTION_PROMPT
)

from app.ai.prompts.jd_prompt import (
    JOB_DESCRIPTION_EXTRACTION_PROMPT
)

load_dotenv()

logger = logging.getLogger(__name__)


class GeminiService:

    client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY")
    )

    @staticmethod
    def _generate_response(prompt: str):

        model_name = os.getenv("GEMINI_MODEL")

        try:

            response = GeminiService.client.models.generate_content(
                model=model_name,
                contents=prompt
            )

            if not response.text:

                logger.error("Gemini returned an empty response.")

                raise HTTPException(
                    status_code=502,
                    detail="Gemini returned an empty response."
                )

            return response

        except HTTPException:
            raise

        except Exception:

            logger.exception("Gemini API request failed.")

            raise HTTPException(
                status_code=503,
                detail="AI service is temporarily unavailable. Please try again in a few moments."
            )

    @staticmethod
    def extract_resume_information(text: str):

        prompt = RESUME_EXTRACTION_PROMPT.format(
            text=text
        )

        response = GeminiService._generate_response(
            prompt
        )

        from app.ai.response_parser import ResponseParser

        parsed_response = ResponseParser.parse(
            response.text
        )

        return parsed_response

    @staticmethod
    def extract_job_description(text: str):

        prompt = JOB_DESCRIPTION_EXTRACTION_PROMPT.format(
            text=text
        )

        response = GeminiService._generate_response(
            prompt
        )

        from app.ai.response_parser import ResponseParser

        parsed_response = ResponseParser.parse(
            response.text
        )

        return parsed_response