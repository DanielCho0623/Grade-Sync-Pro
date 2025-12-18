import os
import requests
from datetime import datetime, timedelta
import random
from flask import current_app
import logging

class BrightspaceService:
    def __init__(self):
        self.base_url = os.getenv('BRIGHTSPACE_BASE_URL', '')
        self.app_id = os.getenv('BRIGHTSPACE_APP_ID', '')
        self.app_key = os.getenv('BRIGHTSPACE_APP_KEY', '')
        self.user_id = os.getenv('BRIGHTSPACE_USER_ID', '')
        self.user_key = os.getenv('BRIGHTSPACE_USER_KEY', '')

        force_synthetic = os.getenv('USE_SYNTHETIC_DATA', 'true').lower() == 'true'
        self.use_synthetic = force_synthetic or not all([self.base_url, self.app_id, self.app_key])

        try:
            if self.use_synthetic:
                if force_synthetic:
                    current_app.logger.info("Brightspace: Using synthetic data (forced by USE_SYNTHETIC_DATA setting)")
                else:
                    current_app.logger.info("Brightspace: Using synthetic data (no API credentials configured)")
            else:
                current_app.logger.info("Brightspace: Real API integration enabled")
        except RuntimeError:
            pass

    def _get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self._get_access_token()}'
        }

    def _get_access_token(self):
        if self.use_synthetic:
            return 'synthetic_token'

        token_url = f'{self.base_url}/d2l/api/lp/auth'
        params = {
            'x_a': self.app_id,
            'x_b': self.user_id,
            'x_c': self.app_key,
            'x_d': self.user_key
        }

        try:
            response = requests.get(token_url, params=params)
            response.raise_for_status()
            return response.json().get('access_token', '')
        except Exception as e:
            current_app.logger.error(f"Brightspace auth error: {e}")
            return ''

    def get_courses(self, user_id):
        if self.use_synthetic:
            return self._generate_synthetic_courses()

        try:
            url = f'{self.base_url}/d2l/api/lp/1.0/enrollments/myenrollments/'
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()

            enrollments = response.json().get('Items', [])
            courses = []

            for enrollment in enrollments:
                org = enrollment.get('OrgUnit', {})
                courses.append({
                    'brightspace_course_id': str(org.get('Id')),
                    'course_code': org.get('Code', ''),
                    'course_name': org.get('Name', ''),
                    'semester': self._extract_semester(org.get('Name', '')),
                    'year': datetime.now().year
                })

            return courses
        except Exception as e:
            current_app.logger.error(f"Brightspace get_courses error: {e}")
            return self._generate_synthetic_courses()

    def get_assignments(self, course_id):
        if self.use_synthetic:
            return self._generate_synthetic_assignments(course_id)

        try:
            url = f'{self.base_url}/d2l/api/le/1.0/{course_id}/activities/'
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()

            activities = response.json()
            assignments = []

            for activity in activities:
                if activity.get('ActivityType') in ['Assignment', 'Quiz']:
                    assignments.append({
                        'brightspace_assignment_id': str(activity.get('Id')),
                        'name': activity.get('Name', ''),
                        'category': activity.get('ActivityType', 'Assignment'),
                        'max_points': float(activity.get('MaxPoints', 100)),
                        'due_date': self._parse_date(activity.get('DueDate')),
                        'description': activity.get('Description', {}).get('Text', '')
                    })

            return assignments
        except Exception as e:
            current_app.logger.error(f"Brightspace get_assignments error: {e}")
            return self._generate_synthetic_assignments(course_id)

    def get_grades(self, course_id, user_id):
        if self.use_synthetic:
            return self._generate_synthetic_grades()

        try:
            url = f'{self.base_url}/d2l/api/le/1.0/{course_id}/grades/values/{user_id}/'
            response = requests.get(url, headers=self._get_headers())
            response.raise_for_status()

            grade_values = response.json()
            grades = {}

            for grade in grade_values:
                assignment_id = str(grade.get('GradeObjectIdentifier'))
                grades[assignment_id] = {
                    'points_earned': float(grade.get('PointsNumerator', 0)),
                    'graded_date': self._parse_date(grade.get('GradedDate')),
                    'feedback': grade.get('Comments', {}).get('Text', '')
                }

            return grades
        except Exception as e:
            current_app.logger.error(f"Brightspace get_grades error: {e}")
            return self._generate_synthetic_grades()

    def _extract_semester(self, course_name):
        if 'Spring' in course_name or 'Sp' in course_name:
            return 'Spring'
        elif 'Summer' in course_name or 'Su' in course_name:
            return 'Summer'
        elif 'Fall' in course_name or 'Fa' in course_name:
            return 'Fall'
        elif 'Winter' in course_name or 'Wi' in course_name:
            return 'Winter'
        return 'Spring'

    def _parse_date(self, date_string):
        if not date_string:
            return None
        try:
            return datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        except:
            return None

    def _generate_synthetic_courses(self):
        current_year = datetime.now().year
        return [
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
                'course_code': 'MATH 2341',
                'course_name': 'Differential Equations',
                'semester': 'Spring',
                'year': current_year
            }
        ]

    def _generate_synthetic_assignments(self, course_id):
        assignments = []
        categories = ['Homework', 'Quiz', 'Exam', 'Project']

        for i in range(1, 8):
            category = categories[i % len(categories)]
            assignments.append({
                'brightspace_assignment_id': f'ASSIGN{i}',
                'name': f'{category} {i}',
                'category': category,
                'max_points': 100 if category != 'Exam' else 200,
                'due_date': datetime.now() + timedelta(days=i*7),
                'description': f'{category} assignment {i} description'
            })
        return assignments

    def _generate_synthetic_grades(self):
        grades = {}
        for i in range(1, 8):
            grades[f'ASSIGN{i}'] = {
                'points_earned': round(random.uniform(75, 100), 2),
                'graded_date': datetime.now() - timedelta(days=random.randint(1, 30)),
                'feedback': random.choice(['Excellent work!', 'Good job!', 'Well done!', 'Keep it up!'])
            }
        return grades
