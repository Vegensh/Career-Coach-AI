from career_data import get_career_info
from difflib import get_close_matches


class CareerCoachBot:
    def __init__(self):
        self.user_states = {}  # For future session/user state

    def detect_intent(self, msg: str, intent_map: dict, cutoff: float = 0.7) -> str:
        """
        Detect the user intent using keywords and fuzzy matching.
        Returns the detected intent or 'summary' as default.
        """
        msg = msg.lower()
        words = msg.split()

        # Direct keyword matching for quick detection
        for intent, keywords in intent_map.items():
            if any(word in msg for word in keywords):
                return intent

        # Fuzzy matching so that user typos can also be recognized
        for user_word in words:
            for intent, keywords in intent_map.items():
                match = get_close_matches(user_word, keywords, n=1, cutoff=cutoff)
                if match:
                    return intent

        return "summary"

    def process_message(self, user_input, sector=None, job=None):
        """
        Processes a user's input and returns a focused answer:
        - salary: returns only salary info,
        - college: returns only college/academy info,
        - roadmap: returns only career steps,
        - company: returns only top employers,
        - courses/skills: gives relevant info,
        - anything else: provides a short summary, not all fields.
        """

        if not sector or not job:
            return (
                "Please specify both the career sector and job for details. For example:\n"
                "sector='Sports & Fitness', job='Cricket'"
            )

        msg = user_input.lower().strip()

        # Define intents with common keywords and common misspellings
        intent_map = {
            "salary": ["salary", "salery", "sallary", "salry", "package", "pay", "wage", "ctc", "income"],
            "college": [
                "college", "colleges", "clg", "university", "universities",
                "academy", "academies", "institute", "instute",
                "school", "which college", "top college", "best college"
            ],
            "roadmap": [
                "roadmap", "road map", "steps", "process", "path",
                "pathway", "progression", "plan", "become",
                "how to start", "how do i become"
            ],
            "company": [
                "company", "companies", "employer", "employers", "firm", "firms",
                "organisation", "organization", "top company", "top companies",
                "leading companies"
            ],
            "courses": [
                "course", "courses", "degree", "degrees",
                "certification", "certifications", "qualification", "qualifications",
                "study", "required course"
            ],
            "skills": [
                "skill", "skills", "requirement", "requirements",
                "competency", "competencies", "necessary skills"
            ],
        }

        detected_intent = self.detect_intent(msg, intent_map)

        # Fetch career info from data
        info = get_career_info(sector, job)
        if not info:
            return f"Sorry, I don't have details for the role '{job}' in sector '{sector}'."

        # Return focused info based on detected intent
        if detected_intent == "salary":
            salary = info.get("average_salary", {})
            fresher = salary.get("fresher", "Data not available")
            experienced = salary.get("experienced", "Data not available")
            return (
                f"**Salary Information for '{job}':**\n"
                f"- Fresher: {fresher}\n"
                f"- Experienced: {experienced}"
            )

        elif detected_intent == "college":
            colleges = info.get("top_colleges") or info.get("top_academies") or {}
            if colleges:
                return (
                    f"**Top Colleges/Academies for '{job}':**\n" +
                    "\n".join(f"- {name}: {desc}" for name, desc in colleges.items())
                )
            return "Sorry, college/academy information is not available."

        elif detected_intent == "roadmap":
            steps = info.get("career_steps", [])
            if steps:
                return (
                    f"**Career Roadmap for '{job}':**\n" +
                    "\n".join(f"{i+1}. {step}" for i, step in enumerate(steps))
                )
            return "Sorry, career steps information is not available."

        elif detected_intent == "company":
            companies = info.get("top_companies") or info.get("top_academies") or {}
            if companies:
                return (
                    f"**Top Employers for '{job}':**\n" +
                    "\n".join(f"- {name}" for name in companies.keys())
                )
            return "Sorry, company information is not available."

        elif detected_intent == "courses":
            courses = info.get("courses", [])
            if courses:
                return (
                    f"**Relevant Courses for '{job}':**\n" +
                    "\n".join(f"- {course}" for course in courses)
                )
            return "Sorry, course information is not available."

        elif detected_intent == "skills":
            skills = info.get("skills_required", [])
            return (
                f"**Key Skills for '{job}':**\n" + (", ".join(skills) if skills else "Skills information not specified.")
            )

        # Default: provide a concise summary without overwhelming details
        summary_parts = []
        if "average_salary" in info:
            salary = info["average_salary"]
            fresher = salary.get("fresher", "N/A")
            experienced = salary.get("experienced", "N/A")
            summary_parts.append(f"Salary (Fresher): {fresher}, (Experienced): {experienced}")
        if "courses" in info:
            summary_parts.append("Courses: " + ", ".join(info["courses"]))
        colleges = info.get("top_colleges") or info.get("top_academies") or {}
        if colleges:
            summary_parts.append("Top Colleges/Academies: " + ", ".join(colleges.keys()))
        companies = info.get("top_companies") or info.get("top_academies") or {}
        if companies:
            summary_parts.append("Top Employers: " + ", ".join(companies.keys()))
        if "career_steps" in info:
            steps = "; ".join(info["career_steps"][:3]) + ("..." if len(info["career_steps"]) > 3 else "")
            summary_parts.append("Roadmap: " + steps)
        if not summary_parts:
            return f"'{job}' is a professional role in the '{sector}' sector."

        return (
            f"**Summary for '{job}':**\n" +
            "\n".join(f"- {line}" for line in summary_parts)
        )
