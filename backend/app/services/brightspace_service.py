import requests
from datetime import datetime, timedelta
import random
from flask import current_app

class BrightspaceService:

    def __init__(self):
        self.base_url = current_app.config.get('BRIGHTSPACE_URL')
        self.client_id = current_app.config.get('BRIGHTSPACE_CLIENT_ID')
        self.client_secret = current_app.config.get('BRIGHTSPACE_CLIENT_SECRET')
        self.use_synthetic = not all([self.base_url, self.client_id, self.client_secret])

    def get_courses(self, user_id):
        if self.use_synthetic:
            return self._generate_synthetic_courses()

        try:
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
        pass

    def _parse_courses(self, data):
        pass

    def _parse_grades(self, data):
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
        grades = {}

        for i in range(1, 6):
            grades[f'HW{i}'] = {
                'points_earned': random.uniform(75, 100),
                'graded_date': datetime.now() - timedelta(days=random.randint(1, 30)),
                'feedback': 'Good work!'
            }

        return grades
