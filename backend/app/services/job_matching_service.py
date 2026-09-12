from app.schemas.resume_schema import ResumeResponse
from app.schemas.jd_schema import JDResponse
from app.schemas.matching_schema import MatchResponse
from app.services.matching_utils import (
    match_skill_list,
    match_education,
    match_experience,
    keyword_matches
)
from app.ai.gemini_service import GeminiService


class JobMatchingService:

    @staticmethod
    def calculate_overall_match(
        required_skill_score: int,
        preferred_skill_score: int,
        education_score: int,
        experience_score: int,
        keyword_score: int,
        semantic_score: int
    ) -> int:

        rule_score = (
            required_skill_score * 0.50
            + preferred_skill_score * 0.10
            + education_score * 0.10
            + experience_score * 0.15
            + keyword_score * 0.15
        )

        return round(rule_score * 0.70 + semantic_score * 0.30)

    @staticmethod
    def generate_suggestions(
        required: dict,
        preferred: dict,
        education: dict,
        experience: dict,
        keywords: dict,
        ai_match
    ) -> list[str]:

        suggestions = []

        for skill in required["missing"]:
            suggestions.append(
                f"Improve your skills in {skill} "
                "to better match the job requirements."
            )

        for skill in required["related"]:
            suggestions.append(
                f"Your {skill} experience is related to "
                f"this requirement. Consider strengthening "
                f"your knowledge of {skill}."
            )

        for skill in preferred["missing"]:
            suggestions.append(
                f"Consider learning {skill} "
                "as it is a preferred skill for this role."
            )

        if not education["match"]:
            suggestions.append(
                "Your education does not fully match "
                "the education requirement for this role."
            )

        if not experience["match"]:
            suggestions.append(
                "Consider gaining more relevant professional "
                "experience to meet the job requirement."
            )

        if keywords["missing"]:
            suggestions.append(
                "Consider adding these missing keywords "
                "where they accurately reflect your experience: "
                + ", ".join(keywords["missing"])
                + "."
            )

        for gap in ai_match.gaps:
            if not any(
                word.lower() in gap.lower()
                for word in ["aws", "git", "education", "experience"]
                if word
            ):
                suggestions.append(gap)

        unique = []

        for suggestion in suggestions:
            if suggestion not in unique:
                unique.append(suggestion)

        return unique[:6] or [
            "Your resume is well aligned with the job description."
        ]

    @staticmethod
    def match(
        resume: ResumeResponse,
        jd: JDResponse
    ) -> MatchResponse:

        required = match_skill_list(
            resume.skills,
            jd.required_skills
        )

        preferred = match_skill_list(
            resume.skills,
            jd.preferred_skills
        )

        education = match_education(
            resume.education,
            jd.education_required
        )

        experience = match_experience(
            resume.experience,
            jd.experience_required
        )

        keywords = keyword_matches(
            resume,
            jd.keywords
        )

        ai_match = GeminiService.analyze_job_match(
            resume.model_dump_json(),
            jd.model_dump_json()
        )

        overall_score = JobMatchingService.calculate_overall_match(
            required["score"],
            preferred["score"],
            education["score"],
            experience["score"],
            keywords["score"],
            ai_match.overall_semantic_match
        )

        suggestions = JobMatchingService.generate_suggestions(
            required,
            preferred,
            education,
            experience,
            keywords,
            ai_match
        )

        return MatchResponse(
            overall_match=overall_score,

            required_skill_match=required["score"],
            preferred_skill_match=preferred["score"],
            education_match=education["match"],
            experience_match=experience["match"],
            keyword_match=keywords["score"],

            matched_required_skills=required["matched"],
            related_required_skills=required["related"],
            missing_required_skills=required["missing"],

            matched_preferred_skills=preferred["matched"],
            related_preferred_skills=preferred["related"],
            missing_preferred_skills=preferred["missing"],

            overall_semantic_match=ai_match.overall_semantic_match,
            experience_relevance=ai_match.experience_relevance,
            project_relevance=ai_match.project_relevance,
            skill_relevance=ai_match.skill_relevance,
            responsibility_alignment=ai_match.responsibility_alignment,

            reasoning=ai_match.reasoning,
            strengths=ai_match.strengths,
            gaps=ai_match.gaps,

            suggestions=suggestions
        )