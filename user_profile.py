from datetime import datetime, timedelta

class UserProfile:
    """User profile management for personalized career guidance"""

    def __init__(self, user_id):
        self.user_id = user_id
        self.name = None
        self.education_status = None  # school/college/graduate/working/gap
        self.current_level = None     # e.g. 10th/12th/undergraduate/postgraduate
        self.current_field = None     # e.g. science/commerce/arts/technical
        self.interests = []
        self.strengths = []
        self.preferred_path = None    # education/sports
        self.career_preferences = {}
        self.assessment_scores = {}
        self.recommended_careers = []
        self.created_at = datetime.now()
        self.last_active = datetime.now()

    def update_last_active(self):
        """Update last active timestamp"""
        self.last_active = datetime.now()

    def add_interest(self, interest):
        """Add unique interest"""
        if interest and interest not in self.interests:
            self.interests.append(interest)

    def add_strength(self, strength):
        """Add unique strength"""
        if strength and strength not in self.strengths:
            self.strengths.append(strength)

    def set_assessment_score(self, category, score):
        """Set score for an assessment category"""
        self.assessment_scores[category] = score

    def get_completion_percentage(self):
        """Calculate profile completion percentage"""
        total_fields = 8
        completed_fields = 0

        if self.name: completed_fields += 1
        if self.education_status: completed_fields += 1
        if self.current_level: completed_fields += 1
        if self.current_field: completed_fields += 1
        if self.preferred_path: completed_fields += 1
        if self.interests: completed_fields += 1
        if self.career_preferences: completed_fields += 1
        if self.assessment_scores: completed_fields += 1

        return int((completed_fields / total_fields) * 100)

    def to_dict(self):
        """Serialize profile to dictionary"""
        return {
            'user_id': self.user_id,
            'name': self.name,
            'education_status': self.education_status,
            'current_level': self.current_level,
            'current_field': self.current_field,
            'interests': self.interests,
            'strengths': self.strengths,
            'preferred_path': self.preferred_path,
            'career_preferences': self.career_preferences,
            'assessment_scores': self.assessment_scores,
            'recommended_careers': self.recommended_careers,
            'completion_percentage': self.get_completion_percentage(),
            'created_at': self.created_at.isoformat(),
            'last_active': self.last_active.isoformat()
        }

    def from_dict(self, data):
        """Load profile from dictionary"""
        self.name = data.get('name')
        self.education_status = data.get('education_status')
        self.current_level = data.get('current_level')
        self.current_field = data.get('current_field')
        self.interests = data.get('interests', [])
        self.strengths = data.get('strengths', [])
        self.preferred_path = data.get('preferred_path')
        self.career_preferences = data.get('career_preferences', {})
        self.assessment_scores = data.get('assessment_scores', {})
        self.recommended_careers = data.get('recommended_careers', [])
        
        if data.get('created_at'):
            self.created_at = datetime.fromisoformat(data['created_at'])
        if data.get('last_active'):
            self.last_active = datetime.fromisoformat(data['last_active'])

    def get_summary(self):
        """Formatted profile summary for quick display"""
        completion = self.get_completion_percentage()
        return f"""
👤 **Your Profile Summary:** ({completion}% Complete)

• **Name:** {self.name or 'Not provided'}
• **Education:** {self.education_status or 'Not specified'} ({self.current_level or 'Not specified'})
• **Field:** {self.current_field or 'Not specified'}
• **Career Path:** {self.preferred_path or 'Not selected'}
• **Interests:** {', '.join(self.interests) if self.interests else 'Not specified'}
• **Strengths:** {', '.join(self.strengths) if self.strengths else 'Not specified'}

🎯 **Recommended Careers:** {', '.join(self.recommended_careers[:3]) if self.recommended_careers else 'Assessment needed'}
        """

    def get_personalized_greeting(self):
        """Return a personalized greeting based on time of day and name"""
        if not self.name:
            return "Hello! I'm excited to help you explore career opportunities!"

        hour = datetime.now().hour
        if hour < 12:
            greeting = "Good morning"
        elif hour < 17:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"

        return f"{greeting}, {self.name}! Ready to explore your career journey today?"

# In-memory user profiles store (replace with DB in production)
USER_PROFILES = {}

def get_user_profile(user_id):
    """Retrieve or create user profile"""
    if user_id not in USER_PROFILES:
        USER_PROFILES[user_id] = UserProfile(user_id)
    else:
        USER_PROFILES[user_id].update_last_active()

    return USER_PROFILES[user_id]

def save_user_profile(profile):
    """Save/update user profile in store"""
    profile.update_last_active()
    USER_PROFILES[profile.user_id] = profile
    return True

def delete_user_profile(user_id):
    """Delete user profile from store"""
    if user_id in USER_PROFILES:
        del USER_PROFILES[user_id]
        return True
    return False
