import re


SKILL_ALIASES = {
    "python 3": "python",
    "python3": "python",
    "reactjs": "react",
    "react.js": "react",
    "nodejs": "node.js",
    "node": "node.js",
    "git hub": "github",
    "amazon web services": "aws",
    "amazon aws": "aws",
    "google cloud platform": "gcp",
    "microsoft azure": "azure",
    "postgres": "postgresql",
    "mongo": "mongodb",
    "sklearn": "scikit-learn",
    "scikit learn": "scikit-learn",
    "rest apis": "rest api",
    "restful api": "rest api",
    "restful apis": "rest api",
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "continuous integration": "ci/cd",
    "continuous delivery": "ci/cd",
}


RELATED_SKILLS = {
    "sql": {"postgresql", "mysql", "sqlite", "oracle"},
    "rest api": {"fastapi", "flask", "django", "express"},
    "machine learning": {"scikit-learn", "tensorflow", "pytorch"},
    "deep learning": {"tensorflow", "pytorch"},
    "data analysis": {"pandas", "numpy"},
    "cloud": {"aws", "azure", "gcp"},
}


EDUCATION_ALIASES = {
    "b.e.": "bachelor",
    "be": "bachelor",
    "b.tech": "bachelor",
    "btech": "bachelor",
    "bachelor of engineering": "bachelor",
    "bachelor of technology": "bachelor",
    "bachelor's degree": "bachelor",
    "bachelors degree": "bachelor",
    "bachelor degree": "bachelor",
    "m.e.": "master",
    "me": "master",
    "m.tech": "master",
    "mtech": "master",
    "master of engineering": "master",
    "master of technology": "master",
    "master's degree": "master",
    "masters degree": "master",
    "master degree": "master",
    "mca": "master",
    "mba": "master",
    "ph.d": "phd",
    "phd": "phd",
    "doctorate": "phd",
}


def normalize_skill(skill: str) -> str:
    skill = skill.lower().strip()
    return SKILL_ALIASES.get(skill, skill)


def match_skill_list(
    resume_skills: list[str],
    job_skills: list[str]
) -> dict:

    resume = {
        normalize_skill(skill)
        for skill in resume_skills
        if skill and skill.strip()
    }

    job = {
        normalize_skill(skill): skill.strip()
        for skill in job_skills
        if skill and skill.strip()
    }

    matched = []
    related = []
    missing = []

    for normalized, original in job.items():

        if normalized in resume:
            matched.append(original)
            continue

        related_found = RELATED_SKILLS.get(normalized, set()) & resume

        if related_found:
            related.append(original)
        else:
            missing.append(original)

    score = 100 if not job else round(
        len(matched) / len(job) * 100
    )

    return {
        "score": score,
        "matched": sorted(matched),
        "related": sorted(related),
        "missing": sorted(missing),
    }


def normalize_education(education: str) -> str:
    education = education.lower().strip()

    for alias, replacement in EDUCATION_ALIASES.items():
        education = education.replace(alias, replacement)

    return re.sub(r"\s+", " ", education)


def education_level(education: str) -> str:
    education = normalize_education(education)

    if "phd" in education:
        return "phd"
    if "master" in education:
        return "master"
    if "bachelor" in education:
        return "bachelor"

    return education


def education_specialization(education: str) -> str:
    education = normalize_education(education)

    patterns = [
        r"\bin\s+(.+)",
        r"\bof\s+(.+)",
        r"\(([^)]+)\)",
    ]

    for pattern in patterns:
        match = re.search(pattern, education)
        if match:
            return match.group(1).strip()

    return ""


def match_education(
    resume_education: list,
    required: str | None
) -> dict:

    if not required:
        return {"match": True, "score": 100}

    required_normalized = normalize_education(required)
    required_level = education_level(required)
    required_specialization = education_specialization(required)

    for education in resume_education:
        degree = normalize_education(education.degree)
        level = education_level(degree)
        specialization = education_specialization(degree)

        if degree == required_normalized:
            return {"match": True, "score": 100}

        if level != required_level:
            continue

        if not required_specialization:
            return {"match": True, "score": 100}

        if specialization:
            if required_specialization in specialization:
                return {"match": True, "score": 100}

    return {"match": False, "score": 0}


def experience_years(experiences: list) -> float:
    total = 0.0

    for experience in experiences:
        text = (experience.duration or "").lower()

        years = re.search(
            r"(\d+(?:\.\d+)?)\s*years?",
            text
        )

        months = re.search(
            r"(\d+(?:\.\d+)?)\s*months?",
            text
        )

        if years:
            total += float(years.group(1))

        if months:
            total += float(months.group(1)) / 12

    return round(total, 1)


def match_experience(
    experiences: list,
    required: str | None
) -> dict:

    requirement = (required or "").lower().strip()

    if not requirement:
        return {"match": True, "score": 100}

    years = experience_years(experiences)

    if "fresher" in requirement:
        matched = years == 0

    else:
        range_match = re.search(
            r"(\d+(?:\.\d+)?)\s*(?:-|to)\s*"
            r"(\d+(?:\.\d+)?)",
            requirement
        )

        plus_match = re.search(
            r"(\d+(?:\.\d+)?)\s*\+",
            requirement
        )

        year_match = re.search(
            r"(\d+(?:\.\d+)?)\s*years?",
            requirement
        )

        if range_match:
            minimum = float(range_match.group(1))
            maximum = float(range_match.group(2))
            matched = minimum <= years <= maximum

        elif plus_match:
            minimum = float(plus_match.group(1))
            matched = years >= minimum

        elif year_match:
            matched = years >= float(year_match.group(1))

        else:
            matched = True

    return {
        "match": matched,
        "score": 100 if matched else 0
    }


def normalize_text(text: str) -> str:

    text = text.lower()

    replacements = {
        r"\brestful\s+apis?\b": "rest api",
        r"\brest\s+apis?\b": "rest api",
        r"\bmicroservices?\b": "microservice",
        r"\bci\s*/?\s*cd\b": "ci/cd",
        r"\bcontinuous\s+integration\b": "ci/cd",
        r"\bcontinuous\s+delivery\b": "ci/cd",
    }

    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text)

    text = re.sub(r"[^a-z0-9+#./-]", " ", text)

    return re.sub(r"\s+", " ", text).strip()


def build_resume_text(resume) -> str:

    parts = [
        resume.summary or "",
        *resume.skills,
        *resume.certifications,
    ]

    for education in resume.education:
        parts.extend([
            education.degree,
            education.institution,
        ])

    for experience in resume.experience:
        parts.extend([
            experience.company,
            experience.designation,
            experience.description,
        ])

    for project in resume.projects:
        parts.extend([
            project.name,
            project.role,
            project.development_environment,
            project.testing_environment,
            project.description,
        ])

    return normalize_text(" ".join(parts))


def keyword_matches(
    resume,
    keywords: list[str]
) -> dict:

    keyword_aliases = {
        "unit testing": {"pytest", "unittest", "testing"},
        "rest api": {"rest api", "fastapi", "flask", "django"},
        "computer science": {"computer science", "computer engineering"},
        "sql": {"sql", "postgresql", "mysql", "sqlite", "oracle"},
    }

    keyword_map = {
        normalize_text(keyword): keyword.strip()
        for keyword in keywords
        if keyword and keyword.strip()
    }

    if not keyword_map:
        return {
            "score": 100,
            "matched": [],
            "missing": [],
        }

    resume_text = build_resume_text(resume)

    matched = []
    missing = []

    for normalized, original in keyword_map.items():

        terms = keyword_aliases.get(
            normalized,
            {normalized}
        )

        found = any(
            re.search(
                rf"(?<!\w){re.escape(term)}(?!\w)",
                resume_text
            )
            for term in terms
        )

        if found:
            matched.append(original)
        else:
            missing.append(original)

    score = round(
        len(matched) / len(keyword_map) * 100
    )

    return {
        "score": score,
        "matched": sorted(matched),
        "missing": sorted(missing),
    }