from app.schemas.resume_schema import ResumeResponse
from app.schemas.jd_schema import JDResponse
from app.schemas.matching_schema import MatchResponse

import re


class JobMatchingService:

    @staticmethod
    def match_required_skills(
        resume: ResumeResponse,
        jd: JDResponse
    ):
        resume_skills = {
            skill.lower().strip()
            for skill in resume.skills
        }
    
        required_skills = {
            skill.lower().strip()
            for skill in jd.required_skills
        }
    
        matched_skills = resume_skills.intersection(
            required_skills
        )
    
        missing_skills = required_skills.difference(
            resume_skills
        )
    
        if not required_skills:
            score = 100
        else:
            score = round(
                (len(matched_skills) / len(required_skills)) * 100
            )
    
        return {
            "score": score,
            "matched": sorted(matched_skills),
            "missing": sorted(missing_skills)
        }


    @staticmethod
    def match_preferred_skills(
        resume: ResumeResponse,
        jd: JDResponse
    ):
        resume_skills = {
            skill.lower().strip()
            for skill in resume.skills
        }
    
        preferred_skills = {
            skill.lower().strip()
            for skill in jd.preferred_skills
        }
    
        matched_skills = resume_skills.intersection(
            preferred_skills
        )
    
        missing_skills = preferred_skills.difference(
            resume_skills
        )
    
        if not preferred_skills:
            score = 100
        else:
            score = round(
                (len(matched_skills) / len(preferred_skills)) * 100
            )
    
        return {
            "score": score,
            "matched": sorted(matched_skills),
            "missing": sorted(missing_skills)
        }


    @staticmethod
    def normalize_education(education: str) -> str:
    
        education = education.lower().strip()
    
        education_mapping = {
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
            "doctorate": "phd"
        }
    
        return education_mapping.get(
            education,
            education
        )


    @staticmethod
    def match_education(
        resume: ResumeResponse,
        jd: JDResponse
    ):
        required_education = jd.education_required.strip()
    
        if not required_education:
            return {
                "match": True,
                "score": 100
            }
    
        normalized_required = (
            JobMatchingService.normalize_education(
                required_education
            )
        )
    
        for education in resume.education:
    
            normalized_degree = (
                JobMatchingService.normalize_education(
                    education.degree
                )
            )
    
            if normalized_degree == normalized_required:
    
                return {
                    "match": True,
                    "score": 100
                }
    
        return {
            "match": False,
            "score": 0
        }


    @staticmethod
    def calculate_resume_experience(
        resume: ResumeResponse
    ) -> float:
        """
        Calculate total years of professional experience
        from the resume.
        """

        total_experience = 0.0

        for experience in resume.experience:

            duration = (
                experience.duration or ""
            ).lower().strip()

            # Handle ranges such as:
            # "1-2 Years"
            # "1 to 2 Years"
            range_match = re.search(
                r"(\d+(?:\.\d+)?)\s*(?:-|to)\s*(\d+(?:\.\d+)?)\s*years?",
                duration
            )

            if range_match:
                start = float(
                    range_match.group(1)
                )

                end = float(
                    range_match.group(2)
                )

                total_experience += max(
                    end - start,
                    0
                )

                continue

            # Handle values such as:
            # "2 Years"
            # "6 Months"
            single_match = re.search(
                r"(\d+(?:\.\d+)?)\s*years?",
                duration
            )

            if single_match:
                total_experience += float(
                    single_match.group(1)
                )

                continue

            # Handle values such as:
            # "6 Months"
            month_match = re.search(
                r"(\d+(?:\.\d+)?)\s*months?",
                duration
            )

            if month_match:
                months = float(
                    month_match.group(1)
                )

                total_experience += months / 12

        return round(
            total_experience,
            1
        )


    @staticmethod
    def match_experience(
        resume: ResumeResponse,
        jd: JDResponse
    ):
        """
        Compare resume experience against
        the experience required by the job description.
        """

        required_experience = (
            jd.experience_required or ""
        ).lower().strip()

        # No experience requirement
        if not required_experience:
            return {
                "match": True,
                "score": 100
            }

        resume_years = (
            JobMatchingService.calculate_resume_experience(
                resume
            )
        )

        # Handle Fresher requirement
        if "fresher" in required_experience:

            if resume_years == 0:
                return {
                    "match": True,
                    "score": 100
                }

            return {
                "match": False,
                "score": 0
            }

        # Handle requirements such as:
        # "2+ Years"
        plus_match = re.search(
            r"(\d+(?:\.\d+)?)\s*\+",
            required_experience
        )

        if plus_match:

            minimum_years = float(
                plus_match.group(1)
            )

            if resume_years >= minimum_years:
                return {
                    "match": True,
                    "score": 100
                }

            return {
                "match": False,
                "score": 0
            }

        # Handle requirements such as:
        # "1-3 Years"
        # "1 to 3 Years"
        range_match = re.search(
            r"(\d+(?:\.\d+)?)\s*(?:-|to)\s*(\d+(?:\.\d+)?)",
            required_experience
        )

        if range_match:

            minimum_years = float(
                range_match.group(1)
            )

            maximum_years = float(
                range_match.group(2)
            )

            if (
                minimum_years
                <= resume_years
                <= maximum_years
            ):
                return {
                    "match": True,
                    "score": 100
                }

            return {
                "match": False,
                "score": 0
            }

        # Handle requirements such as:
        # "3 Years"
        single_match = re.search(
            r"(\d+(?:\.\d+)?)\s*years?",
            required_experience
        )

        if single_match:

            required_years = float(
                single_match.group(1)
            )

            if resume_years >= required_years:
                return {
                    "match": True,
                    "score": 100
                }

            return {
                "match": False,
                "score": 0
            }

       
        return {
            "match": True,
            "score": 100
        }


    @staticmethod
    def match_keywords(
        resume: ResumeResponse,
        jd: JDResponse
    ):
        """
        Match JD keywords against the text
        available in the resume.
        """

        keywords = {
            keyword.lower().strip()
            for keyword in jd.keywords
            if keyword.strip()
        }

        # If JD has no keywords, consider it a full match
        if not keywords:
            return {
                "score": 100,
                "matched": [],
                "missing": []
            }

        resume_text_parts = []

        # Resume summary
        if resume.summary:
            resume_text_parts.append(
                resume.summary
            )

        # Resume skills
        resume_text_parts.extend(
            resume.skills
        )

        # Resume experience
        for experience in resume.experience:

            resume_text_parts.extend([
                experience.designation,
                experience.company,
                experience.description
            ])

        # Resume projects
        for project in resume.projects:

            resume_text_parts.extend([
                project.name,
                project.role,
                project.development_environment,
                project.testing_environment,
                project.description
            ])

        # Combine all resume text
        resume_text = " ".join(
            str(part)
            for part in resume_text_parts
            if part
        ).lower()

        matched_keywords = set()
        missing_keywords = set()

        for keyword in keywords:

            if keyword in resume_text:
                matched_keywords.add(keyword)
            else:
                missing_keywords.add(keyword)

        score = round(
            (
                len(matched_keywords)
                / len(keywords)
            ) * 100
        )

        return {
            "score": score,
            "matched": sorted(matched_keywords),
            "missing": sorted(missing_keywords)
        }



    @staticmethod
    def generate_suggestions(
        required_skill_result: dict,
        preferred_skill_result: dict,
        education_result: dict,
        experience_result: dict,
        keyword_result: dict
    ):
        """
        Generate actionable suggestions based on
        the individual matching results.
        """

        suggestions = []

        # Required skills
        missing_required_skills = (
            required_skill_result.get("missing", [])
        )

        for skill in missing_required_skills:
            suggestions.append(
                f"Improve your skills in {skill} "
                f"to better match the job requirements."
            )

        # Preferred skills
        missing_preferred_skills = (
            preferred_skill_result.get("missing", [])
        )

        for skill in missing_preferred_skills:
            suggestions.append(
                f"Consider learning {skill} "
                f"as it is a preferred skill for this role."
            )

        # Education
        if not education_result.get("match", True):
            suggestions.append(
                "Your education does not fully match "
                "the education requirement for this role."
            )

        # Experience
        if not experience_result.get("match", True):
            suggestions.append(
                "Consider gaining more relevant professional "
                "experience to meet the job requirement."
            )

        # Keywords
        missing_keywords = (
            keyword_result.get("missing", [])
        )

        if missing_keywords:
            suggestions.append(
                "Consider strengthening your resume with "
                "relevant experience in: "
                + ", ".join(missing_keywords)
                + "."
            )

        # Default message
        if not suggestions:
            suggestions.append(
                "Your resume is well aligned with "
                "the job description."
            )

        return suggestions


    @staticmethod
    def calculate_overall_match(
        required_skill_score: int,
        preferred_skill_score: int,
        education_score: int,
        experience_score: int,
        keyword_score: int
    ) -> int:
        """
        Calculate the overall job match score
        using weighted individual scores.
        """

        overall_score = (
            required_skill_score * 0.50
            + preferred_skill_score * 0.10
            + education_score * 0.10
            + experience_score * 0.15
            + keyword_score * 0.15
        )

        return round(overall_score)


    @staticmethod
    def match(
        resume: ResumeResponse,
        jd: JDResponse
    ) -> MatchResponse:

        # 1. Required skill matching
        required_skill_result = (
            JobMatchingService.match_required_skills(
                resume,
                jd
            )
        )

        # 2. Preferred skill matching
        preferred_skill_result = (
            JobMatchingService.match_preferred_skills(
                resume,
                jd
            )
        )

        # 3. Education matching
        education_result = (
            JobMatchingService.match_education(
                resume,
                jd
            )
        )

        # 4. Experience matching
        experience_result = (
            JobMatchingService.match_experience(
                resume,
                jd
            )
        )

        # 5. Keyword matching
        keyword_result = (
            JobMatchingService.match_keywords(
                resume,
                jd
            )
        )

        # 6. Calculate overall score
        overall_score = (
            JobMatchingService.calculate_overall_match(
                required_skill_score=required_skill_result["score"],
                preferred_skill_score=preferred_skill_result["score"],
                education_score=education_result["score"],
                experience_score=experience_result["score"],
                keyword_score=keyword_result["score"]
            )
        )

        # 7. Generate suggestions
        suggestions = (
            JobMatchingService.generate_suggestions(
                required_skill_result=required_skill_result,
                preferred_skill_result=preferred_skill_result,
                education_result=education_result,
                experience_result=experience_result,
                keyword_result=keyword_result
            )
        )

        # 8. Build final response
        return MatchResponse(
            overall_match=overall_score,

            required_skill_match=(
                required_skill_result["score"]
            ),

            preferred_skill_match=(
                preferred_skill_result["score"]
            ),

            education_match=(
                education_result["match"]
            ),

            experience_match=(
                experience_result["match"]
            ),

            keyword_match=(
                keyword_result["score"]
            ),

            matched_required_skills=(
                required_skill_result["matched"]
            ),

            missing_required_skills=(
                required_skill_result["missing"]
            ),

            matched_preferred_skills=(
                preferred_skill_result["matched"]
            ),

            missing_preferred_skills=(
                preferred_skill_result["missing"]
            ),

            suggestions=suggestions
        )