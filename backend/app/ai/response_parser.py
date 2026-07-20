import json


class ResponseParser:

    @staticmethod
    def parse(response: str) -> dict:
        """
        Convert Gemini response into a Python dictionary.
        """

        response = response.strip()

        # Remove markdown code block if Gemini returns it
        if response.startswith("```json"):
            response = response.replace("```json", "", 1)

        if response.endswith("```"):
            response = response[:-3]

        response = response.strip()

        return json.loads(response)