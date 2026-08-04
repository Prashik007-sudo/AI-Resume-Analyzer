JOB_DESCRIPTION_EXTRACTION_PROMPT = """
You are an expert AI Job Description Parser.

Analyze the following job description carefully.

Assume the job description may contain company introductions, marketing content, benefits, culture descriptions, legal statements, and other non-essential information.

Extract ONLY the information that is relevant for evaluating a candidate's suitability for the job.

Return ONLY valid JSON.

IMPORTANT RULES:

1. Return ONLY valid JSON.
2. Do NOT return markdown.
3. Do NOT wrap JSON inside ``` blocks.
4. Do NOT write explanations.
5. Do NOT add extra fields.
6. Every field in the schema must exist.
7. If information is unavailable:
   - Use "" for strings.
   - Use [] for arrays.

Return JSON in EXACTLY this format:

{{
    "job_title": "",
    "company": "",
    "location": "",
    "employment_type": "",
    "experience_required": "",
    "education_required": "",

    "required_skills": [
        ""
    ],

    "preferred_skills": [
        ""
    ],

    "responsibilities": [
        ""
    ],

    "qualifications": [
        ""
    ],

    "keywords": [
        ""
    ]
}}

-------------------------
EXTRACTION RULES
-------------------------

JOB TITLE

- Extract only the job title.

COMPANY

- Extract only the company name.

LOCATION

- Extract the job location if available.

EMPLOYMENT TYPE

Return only one of the following whenever possible:

- Internship
- Full Time
- Part Time
- Contract
- Freelance
- Remote
- Hybrid
- Onsite

If unavailable, return "".

EXPERIENCE REQUIRED

Examples:

- Fresher
- 0-1 Years
- 1-3 Years
- 2+ Years
- 5 Years

EDUCATION REQUIRED

Examples:

- B.Tech
- BE
- BCA
- MCA
- M.Tech
- Master's Degree
- Bachelor's Degree

REQUIRED SKILLS

Extract ONLY mandatory technical skills.

Examples:

- Python
- Java
- FastAPI
- Docker
- Kubernetes
- SQL
- AWS

Rules:

- Return each skill only once.
- Do not include duplicate skills.
- Normalize common skill names.

Examples:

- ReactJS → React
- NodeJS → Node.js
- Git Hub → GitHub
- Amazon Web Services → AWS
- Google Cloud Platform → GCP

PREFERRED SKILLS

Extract skills mentioned as:

- Preferred
- Nice to Have
- Good to Have
- Bonus
- Plus

Rules:

- Return each skill only once.
- Do not include duplicate skills.
- Normalize common skill names.

RESPONSIBILITIES

Extract every major job responsibility.

Rules:

- Return each responsibility as a separate list item.
- Keep responsibilities concise.
- Do not merge multiple responsibilities into one item.

QUALIFICATIONS

Extract qualifications separately.

Examples:

- Excellent communication skills
- Problem solving
- Teamwork
- Leadership
- Analytical thinking

Rules:

- Return one qualification per list item.
- Do not merge multiple qualifications.

KEYWORDS

Extract important ATS keywords that are NOT already included in
required_skills or preferred_skills.

Examples:

- REST API
- Microservices
- CI/CD
- Agile
- Scrum
- Cloud
- DevOps
- AI
- Machine Learning
- Deep Learning
- Problem Solving
- Communication

Rules:

- Do not include duplicate keywords.
- Do not repeat skills already present in required_skills or preferred_skills.

Job Description:

{text}
"""