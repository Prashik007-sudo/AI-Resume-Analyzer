from app.schemas.resume_schema import ResumeResponse
from app.schemas.ats_schema import (
    ATSScoreResponse,
    ScoreBreakdown,
    SectionScore,
)

from app.config.ats_config import (
    CONTACT_POINTS,
    EDUCATION_POINTS,
    EXPERIENCE_POINTS,
    PROJECT_POINTS,
    CERTIFICATION_POINTS,
    SUMMARY_POINTS,
)
from app.config.skill_categories import SKILL_CATEGORIES


class ATSScoreService:

    @staticmethod
    def score_contact(resume: ResumeResponse) -> SectionScore:
    
        score = 0
        suggestions = []
    
        if resume.email:
            score += CONTACT_POINTS["email"]
        else:
            suggestions.append("Add a professional email address.")

    
        if resume.phone:
            score += CONTACT_POINTS["phone"]
        else:
            suggestions.append("Add a phone number.")

    
        if resume.linkedin:
            score += CONTACT_POINTS["linkedin"]
        else:
            suggestions.append("Add your LinkedIn profile.")

    
        if resume.github:
            score += CONTACT_POINTS["github"]
        else:
            suggestions.append("Add your GitHub profile.")

    
        if resume.portfolio:
            score += CONTACT_POINTS["portfolio"]
        else:
            suggestions.append("Add a portfolio or personal website.")
    
        return SectionScore(
            score=score,
            suggestions=suggestions
        )


    @staticmethod
    def score_skills(resume: ResumeResponse) -> SectionScore:
    
        score = 0
        suggestions = []
    
        resume_skills = {
            skill.lower().strip()
            for skill in resume.skills
        }
    
        technical_skill_count = 0
        matched_categories = set()
    
        for category, category_skills in SKILL_CATEGORIES.items():
    
            matched = resume_skills.intersection(category_skills)
    
            if matched:
    
                matched_categories.add(category)
    
                if category != "soft_skills":
                    technical_skill_count += len(matched)
    
        # ----------------------------
        # Technical Skill Depth (12)
        # ----------------------------
    
        if technical_skill_count >= 12:
            score += 12
        elif technical_skill_count >= 8:
            score += 10
        elif technical_skill_count >= 5:
            score += 8
        elif technical_skill_count >= 3:
            score += 5
        elif technical_skill_count >= 1:
            score += 2
        else:
            suggestions.append(
                "Add more technical skills relevant to your target role."
            )
    
        # ----------------------------
        # Category Coverage (8)
        # ----------------------------
    
        category_count = len(matched_categories)
    
        if category_count >= 6:
            score += 8
        elif category_count >= 5:
            score += 7
        elif category_count >= 4:
            score += 6
        elif category_count >= 3:
            score += 4
        elif category_count >= 2:
            score += 2
        else:
            suggestions.append(
                "Diversify your skill set across multiple technology domains."
            )
    
        return SectionScore(
            score=score,
            suggestions=suggestions
        )


    @staticmethod
    def _has_value(value) -> bool:
    
        if value is None:
            return False
    
        if isinstance(value, str):
            return bool(value.strip())
    
        return bool(value)


    @staticmethod
    def score_education(resume: ResumeResponse) -> SectionScore:
    
        score = 0
        suggestions = []
    
        if not resume.education:
            suggestions.append(
                "Add your educational qualifications."
            )
    
            return SectionScore(
                score=0,
                suggestions=suggestions
            )
    
        score += EDUCATION_POINTS["base"]
    
        for education in resume.education:
    
            if ATSScoreService._has_value(education.degree):
                score += EDUCATION_POINTS["degree"]
    
            if ATSScoreService._has_value(education.institution):
                score += EDUCATION_POINTS["institution"]
    
            if ATSScoreService._has_value(education.year):
                score += EDUCATION_POINTS["year"]
    
            if ATSScoreService._has_value(education.percentage):
                score += EDUCATION_POINTS["percentage"]
    
            break
    
        score = min(score, 15)
    
        if score < 10:
            suggestions.append(
                "Provide more complete education details."
            )
    
        return SectionScore(
            score=score,
            suggestions=suggestions
        )


    @staticmethod
    def score_experience(resume: ResumeResponse) -> SectionScore:
    
        score = 0
        suggestions = []
    
        if not resume.experience:
            suggestions.append(
                "Add your work experience or internships."
            )
    
            return SectionScore(
                score=0,
                suggestions=suggestions
            )
    
    
        experience = resume.experience[0]
    
        if ATSScoreService._has_value(experience.company):
            score += EXPERIENCE_POINTS["company"]
    
        if ATSScoreService._has_value(experience.designation):
            score += EXPERIENCE_POINTS["designation"]
    
        if ATSScoreService._has_value(experience.duration):
            score += EXPERIENCE_POINTS["duration"]
    
        if ATSScoreService._has_value(experience.description):
            score += EXPERIENCE_POINTS["description"]
    
        if len(resume.experience) > 1:
            score += EXPERIENCE_POINTS["multiple_experiences"]
    
        score = min(score, 25)
    
        if score < 15:
            suggestions.append(
                "Provide more detailed work experience."
            )
    
        return SectionScore(
            score=score,
            suggestions=suggestions
        )


    @staticmethod
    def score_projects(resume: ResumeResponse) -> SectionScore:
    
        score = 0
        suggestions = []
    
        if not resume.projects:
            suggestions.append(
                "Add academic or personal projects."
            )
    
            return SectionScore(
                score=0,
                suggestions=suggestions
            )
    
        score += PROJECT_POINTS["base"]
    
        project = resume.projects[0]
    
        if ATSScoreService._has_value(project.role):
            score += PROJECT_POINTS["role"]
    
        if ATSScoreService._has_value(project.description):
            score += PROJECT_POINTS["description"]
    
        if ATSScoreService._has_value(project.development_environment):
            score += PROJECT_POINTS["development_environment"]
    
        if ATSScoreService._has_value(project.testing_environment):
            score += PROJECT_POINTS["testing_environment"]
    
        if len(resume.projects) > 1:
            score += PROJECT_POINTS["multiple_projects"]
    
        score = min(score, 15)
    
        if score < 10:
            suggestions.append(
                "Provide more detailed project information."
            )
    
        return SectionScore(
            score=score,
            suggestions=suggestions
        )


    @staticmethod
    def score_certifications(resume: ResumeResponse) -> SectionScore:
    
        score = 0
        suggestions = []
    
        certification_count = len(resume.certifications)
    
        if certification_count == 0:
    
            suggestions.append(
                "Add relevant certifications to strengthen your resume."
            )
    
        elif certification_count == 1:
    
            score = CERTIFICATION_POINTS["single"]
    
        else:
    
            score = CERTIFICATION_POINTS["multiple"]
    
        return SectionScore(
            score=score,
            suggestions=suggestions
        )


    @staticmethod
    def score_summary(resume: ResumeResponse) -> SectionScore:
    
        score = 0
        suggestions = []
    
        if not ATSScoreService._has_value(resume.summary):
    
            suggestions.append(
                "Add a professional resume summary."
            )
    
            return SectionScore(
                score=0,
                suggestions=suggestions
            )
    
        score += SUMMARY_POINTS["present"]
    
        summary_length = len(resume.summary.split())
    
        if summary_length >= 50:
    
            score += SUMMARY_POINTS["excellent_length"]
    
        elif summary_length >= 25:
    
            score += SUMMARY_POINTS["good_length"]
    
        else:
    
            suggestions.append(
                "Expand your professional summary with more relevant information."
            )
    
        score = min(score, 10)
    
        return SectionScore(
            score=score,
            suggestions=suggestions
        )



    @staticmethod
    def calculate_score(resume: ResumeResponse) -> ATSScoreResponse:
    
        contact = ATSScoreService.score_contact(resume)
        skills = ATSScoreService.score_skills(resume)
        education = ATSScoreService.score_education(resume)
        experience = ATSScoreService.score_experience(resume)
        projects = ATSScoreService.score_projects(resume)
        certifications = ATSScoreService.score_certifications(resume)
        summary = ATSScoreService.score_summary(resume)
    
        breakdown = ScoreBreakdown(
            contact=contact.score,
            skills=skills.score,
            education=education.score,
            experience=experience.score,
            projects=projects.score,
            certifications=certifications.score,
            summary=summary.score,
        )
    
        overall_score = (
            contact.score
            + skills.score
            + education.score
            + experience.score
            + projects.score
            + certifications.score
            + summary.score
        )
    
        suggestions = []
    
        suggestions.extend(contact.suggestions)
        suggestions.extend(skills.suggestions)
        suggestions.extend(education.suggestions)
        suggestions.extend(experience.suggestions)
        suggestions.extend(projects.suggestions)
        suggestions.extend(certifications.suggestions)
        suggestions.extend(summary.suggestions)
    
        return ATSScoreResponse(
            overall_score=overall_score,
            breakdown=breakdown,
            suggestions=suggestions,
        )