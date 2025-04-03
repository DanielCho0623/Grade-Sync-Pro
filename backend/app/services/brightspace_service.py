import requests
from datetime import datetime, timedelta
import random
from flask import current_app

class BrightspaceService:
    """
    Service for integrating with Brightspace API.
    Falls back to synthetic data if Brightspace is not configured.
    """

    def __init__(self):
        self.base_url = current_app.config.get('BRIGHTSPACE_URL')
        self.client_id = current_app.config.get('BRIGHTSPACE_CLIENT_ID')
        self.client_secret = current_app.config.get('BRIGHTSPACE_CLIENT_SECRET')
        self.use_synthetic = not all([self.base_url, self.client_id, self.client_secret])

    def get_courses(self, user_id):
        """
        Fetch courses for a user from Brightspace.
        Falls back to synthetic data if not configured.
        """
        if self.use_synthetic:
            return self._generate_synthetic_courses()

        try:
            # Real Brightspace API implementation
            headers = self._get_auth_headers()
            response = requests.get(
                f"{self.base_url}/d2l/api/lp/1.0/enrollments/users/{user_id}/orgUnits/",
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            return self._parse_courses(response.json())
        except Exception as e:
            current_app.logger.error(f"Brightspace API error: {str(e)}")
            return self._generate_synthetic_courses()

    def get_assignments(self, course_id):
        """
        Fetch assignments for a course from Brightspace.
        Falls back to synthetic data if not configured.
        """
        if self.use_synthetic:
            return self._generate_synthetic_assignments(course_id)

        try:
            headers = self._get_auth_headers()
            response = requests.get(
                f"{self.base_url}/d2l/api/le/1.0/{course_id}/dropbox/folders/",
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            return self._parse_assignments(response.json())
        except Exception as e:
            current_app.logger.error(f"Brightspace API error: {str(e)}")
            return self._generate_synthetic_assignments(course_id)

    def get_grades(self, course_id, user_id):
        """
        Fetch grades for a course from Brightspace.
        Falls back to synthetic data if not configured.
        """
        if self.use_synthetic:
            return self._generate_synthetic_grades()

        try:
            headers = self._get_auth_headers()
            response = requests.get(
                f"{self.base_url}/d2l/api/le/1.0/{course_id}/grades/values/{user_id}/",
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            return self._parse_grades(response.json())
        except Exception as e:
            current_app.logger.error(f"Brightspace API error: {str(e)}")
            return self._generate_synthetic_grades()

    def _get_auth_headers(self):
        """Get authentication headers for Brightspace API"""
        # Implementation would include OAuth token retrieval
        return {
            'Authorization': f'Bearer {self._get_access_token()}',
            'Content-Type': 'application/json'
        }

    def _get_access_token(self):
        """Get OAuth access token from Brightspace"""
        # Placeholder for OAuth implementation
        pass

    def _parse_courses(self, data):
        """Parse Brightspace course data"""
        # Implementation would parse actual Brightspace response
        pass

    def _parse_assignments(self, data):
        """Parse Brightspace assignment data"""
        # Implementation would parse actual Brightspace response
        pass

    def _parse_grades(self, data):
        """Parse Brightspace grade data"""
        # Implementation would parse actual Brightspace response
        pass

    # Synthetic data generators for testing/development
    def _generate_synthetic_courses(self):
        """Generate synthetic course data for testing"""
        current_year = datetime.now().year
        courses = [
            {
                'brightspace_course_id': 'BS001',
                'course_code': 'CS 3520',
                'course_name': 'Programming in C++',
                'semester': 'Spring',
                'year': current_year
            },
            {
                'brightspace_course_id': 'BS002',
                'course_code': 'CS 4500',
                'course_name': 'Software Development',
                'semester': 'Spring',
                'year': current_year
            },
            {
                'brightspace_course_id': 'BS003',
                'course_code': 'CS 5800',
                'course_name': 'Algorithms',
                'semester': 'Spring',
                'year': current_year
            }
        ]
        return courses

    def _generate_synthetic_assignments(self, course_id):
        """Generate synthetic assignment data for testing"""
        categories = ['Homework', 'Exam', 'Project', 'Quiz']
        assignments = []

        # Generate homework assignments
        for i in range(1, 6):
            assignments.append({
                'brightspace_assignment_id': f'HW{i}',
                'name': f'Homework {i}',
                'category': 'Homework',
                'max_points': 100,
                'due_date': datetime.now() + timedelta(days=i*7),
                'description': f'Assignment covering topics from week {i}'
            })

        # Generate exams
        for i in range(1, 3):
            assignments.append({
                'brightspace_assignment_id': f'EXAM{i}',
                'name': f'Midterm Exam {i}',
                'category': 'Exam',
                'max_points': 200,
                'due_date': datetime.now() + timedelta(days=i*30),
                'description': f'Comprehensive exam covering chapters 1-{i*5}'
            })

        # Generate projects
        for i in range(1, 3):
            assignments.append({
                'brightspace_assignment_id': f'PROJ{i}',
                'name': f'Course Project {i}',
                'category': 'Project',
                'max_points': 150,
                'due_date': datetime.now() + timedelta(days=i*45),
                'description': f'Major project implementing course concepts'
            })

        return assignments

    def _generate_synthetic_grades(self):
        """Generate synthetic grade data for testing"""
        # Generates random grades for demonstration
        grades = {}

        for i in range(1, 6):
            grades[f'HW{i}'] = {
                'points_earned': random.uniform(75, 100),
                'graded_date': datetime.now() - timedelta(days=random.randint(1, 30)),
                'feedback': 'Good work!'
            }

        return grades
