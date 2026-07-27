RESUME_EXTRACTION_PROMPT = """
You are an expert ATS Resume Parser.

Analyze the resume carefully and extract information into the JSON format below.

IMPORTANT RULES:

1. Return ONLY valid JSON.
2. Do NOT return markdown.
3. Do NOT wrap the JSON inside ``` blocks.
4. Do NOT write explanations.
5. Do NOT add fields that are not in the schema.
6. Every key in the schema must exist.
7. If information is missing, use:
   - "" for strings
   - [] for arrays

Return JSON in EXACTLY this format:

{{
    "name": "",
    "skills": [
        ""
    ],

    "education": [
        {{
            "degree": "",
            "institution": "",
            "year": "",
            "percentage": ""
        }}
    ],

    "experience": [
        {{
            "company": "",
            "designation": "",
            "duration": "",
            "description": ""
        }}
    ],

    "projects": [
        {{
            "name": "",
            "role": "",
            "duration": "",
            "development_environment": "",
            "testing_environment": "",
            "description": ""
        }}
    ],

    "certifications": [
        ""
    ],

    "summary": ""
}}

Extraction Rules

NAME
- Full candidate name only.

SKILLS
- Return every technical skill separately.
- Example:
["Python", "FastAPI", "React"]

EDUCATION
For every education entry extract:
- degree
- institution
- year
- percentage

If percentage is unavailable use "".

EXPERIENCE
For every work experience extract:
- company
- designation
- duration
- description

PROJECTS
For every project extract:
- name
- role
- duration
- development_environment
- testing_environment
- description

If development or testing environment is not mentioned, use "".

CERTIFICATIONS
Return each certification as a separate string.

SUMMARY
Return a professional summary in 2–4 sentences.

Resume:

{text}
"""