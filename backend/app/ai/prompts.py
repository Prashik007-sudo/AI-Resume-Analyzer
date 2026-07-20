RESUME_EXTRACTION_PROMPT = """
You are an expert ATS Resume Parser.

Analyze the resume carefully.

Extract the following information.

Return ONLY valid JSON.

Schema:

{{
    "name": "",
    "skills": [],
    "education": [],
    "experience": [],
    "projects": [],
    "certifications": [],
    "summary": ""
}}

Rules:

- Do not return markdown.
- Do not write explanations.
- Do not add extra fields.
- If a field is missing, return an empty string or empty list.

Resume:

{text}
"""