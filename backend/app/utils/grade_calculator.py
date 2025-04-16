from app.models.assignment import Assignment
from app.models.grade import Grade
from app.models.syllabus_weight import SyllabusWeight

class GradeCalculator:

    @staticmethod
    def calculate_category_average(assignments, category):
        Calculate the final grade for a course based on syllabus weights.
        Returns a dictionary with detailed grade breakdown.
        if percentage is None:
            return None

        if percentage >= 93:
            return 'A'
        elif percentage >= 90:
            return 'A-'
        elif percentage >= 87:
            return 'B+'
        elif percentage >= 83:
            return 'B'
        elif percentage >= 80:
            return 'B-'
        elif percentage >= 77:
            return 'C+'
        elif percentage >= 73:
            return 'C'
        elif percentage >= 70:
            return 'C-'
        elif percentage >= 67:
            return 'D+'
        elif percentage >= 63:
            return 'D'
        elif percentage >= 60:
            return 'D-'
        else:
            return 'F'

    @staticmethod
    def calculate_grade_needed(course, target_grade):
        current_grade_data = GradeCalculator.calculate_course_grade(course)

        if current_grade_data['final_grade'] is None:
            return {
                'target_grade': target_grade,
                'current_grade': 0,
                'remaining_weight': 100,
                'needed_average': target_grade,
                'is_achievable': True
            }

        total_weight_applied = current_grade_data['total_weight_applied']
        remaining_weight = 100 - total_weight_applied

        if remaining_weight <= 0:
            return {
                'target_grade': target_grade,
                'current_grade': current_grade_data['final_grade'],
                'remaining_weight': 0,
                'needed_average': None,
                'is_achievable': current_grade_data['final_grade'] >= target_grade
            }

        current_points = current_grade_data['final_grade']
        needed_points = target_grade - current_points
        needed_average = (needed_points / remaining_weight) * 100

        return {
            'target_grade': target_grade,
            'current_grade': round(current_grade_data['final_grade'], 2),
            'remaining_weight': remaining_weight,
            'needed_average': round(needed_average, 2),
            'is_achievable': needed_average <= 100
        }
