from app.schemas.resume_schema import ResumeResponse
from app.schemas.jd_schema import JDResponse
from app.schemas.matching_schema import MatchResponse

from app.services.matching_utils import (
    match_skill_list,
    match_education,
    match_experience,
    keyword_matches
)


class JobMatchingService:

    @staticmethod
    def calculate_overall_match(
        required_skill_score: int,
        preferred_skill_score: int,
        education_score: int,
        experience_score: int,
        keyword_score: int
    ) -> int:

        return round(
            required_skill_score * 0.50
            + preferred_skill_score * 0.10
            + education_score * 0.10
            + experience_score * 0.15
            + keyword_score * 0.15
        )

    @staticmethod
    def generate_suggestions(
        required: dict,
        preferred: dict,
        education: dict,
        experience: dict,
        keywords: dict
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
                "this requirement. Consider strengthening "
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
                "Consider strengthening your resume with "
                "relevant experience in: "
                + ", ".join(keywords["missing"])
                + "."
            )

        if not suggestions:
            suggestions.append(
                "Your resume is well aligned with "
                "the job description."
            )

        return suggestions

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

        overall_score = JobMatchingService.calculate_overall_match(
            required["score"],
            preferred["score"],
            education["score"],
            experience["score"],
            keywords["score"]
        )

        suggestions = JobMatchingService.generate_suggestions(
            required,
            preferred,
            education,
            experience,
            keywords
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

            suggestions=suggestions
        )