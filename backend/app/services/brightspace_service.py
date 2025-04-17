from datetime import datetime, timedelta
import random
from flask import current_app

class BrightspaceService:
    def __init__(self):
        self.use_synthetic = True

    def get_courses(self, user_id):
        return self._generate_synthetic_courses()

    def get_assignments(self, course_id):
        return self._generate_synthetic_assignments(course_id)

    def get_grades(self, course_id, user_id):
        return self._generate_synthetic_grades()

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
            }
        ]

    def _generate_synthetic_assignments(self, course_id):
        assignments = []
        for i in range(1, 6):
            assignments.append({
                'brightspace_assignment_id': f'HW{i}',
                'name': f'Homework {i}',
                'category': 'Homework',
                'max_points': 100,
                'due_date': datetime.now() + timedelta(days=i*7),
                'description': f'Assignment {i}'
            })
        return assignments

    def _generate_synthetic_grades(self):
        grades = {}
        for i in range(1, 6):
            grades[f'HW{i}'] = {
                'points_earned': random.uniform(75, 100),
                'graded_date': datetime.now() - timedelta(days=random.randint(1, 30)),
                'feedback': 'Good work!'
            }
        return grades
