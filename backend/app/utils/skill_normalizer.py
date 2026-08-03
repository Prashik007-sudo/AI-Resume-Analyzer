class SkillNormalizer:

    SKILL_ALIASES = {

    # Programming Languages
    "cpp": "c++",
    "c plus plus": "c++",
    "js": "javascript",
    "ts": "typescript",
    "py": "python",

    # Frontend
    "reactjs": "react",
    "react.js": "react",
    "nextjs": "next.js",
    "vuejs": "vue",
    "nodejs": "node.js",
    "node js": "node.js",

    # Backend
    "restful api": "rest api",
    "rest apis": "rest api",

    # Databases
    "postgres": "postgresql",
    "ms sql": "sql server",
    "mssql": "sql server",

    # AI / ML
    "machine learning": "ml",
    "deep learning": "dl",
    "large language models": "llm",
    "retrieval augmented generation": "rag",

    # Data Science
    "data structures and algorithms": "dsa",
    "data structures & algorithms": "dsa",
    "data structures and algorithms (dsa)": "dsa",
    "exploratory data analysis": "eda",

    # Version Control
    "git hub": "github",

    # Testing
    "selenium webdriver": "selenium",

    # Cloud
    "amazon web services": "aws",
    "google cloud platform": "gcp",
    "microsoft azure": "azure"
}

    @staticmethod
    def normalize(skill: str) -> str:

        skill = skill.strip().lower()

        return SkillNormalizer.SKILL_ALIASES.get(
            skill,
            skill
        )