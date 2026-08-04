from app.ai.gemini_service import GeminiService

from app.schemas.jd_schema import JDResponse

class JDService:

    @staticmethod
    def extract_job_description(text: str):

        ai_data = GeminiService.extract_job_description(text)

        job_description = JDResponse(

            raw_text=text,

            **ai_data

        )

        return job_description