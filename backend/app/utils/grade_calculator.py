from app.models.assignment import Assignment
from app.models.grade import Grade
from app.models.syllabus_weight import SyllabusWeight

class GradeCalculator:

    @staticmethod
    def calculate_category_average(assignments, category):
        category_assignments = [a for a in assignments if a.category == category and a.grade]
        if not category_assignments:
            return None
        total_points = 0
        earned_points = 0
        for assignment in category_assignments:
            if assignment.grade and assignment.grade.points_earned is not None:
                total_points += assignment.max_points
                earned_points += assignment.grade.points_earned
        if total_points == 0:
            return None
        return (earned_points / total_points) * 100

    @staticmethod
    def calculate_course_grade(course):
        syllabus_weights = course.syllabus_weights
        assignments = course.assignments
        if not syllabus_weights:
            return {
                'final_grade': None,
                'letter_grade': None,
                'breakdown': [],
                'error': 'No syllabus weights defined for this course'
            }
        total_weight = sum(w.weight for w in syllabus_weights)
        if abs(total_weight - 100.0) > 0.01:
            return {
                'final_grade': None,
                'letter_grade': None,
                'breakdown': [],
                'error': f'Syllabus weights must sum to 100% (currently {total_weight}%)'
            }
        breakdown = []
        weighted_grade = 0.0
        total_weight_applied = 0.0
        for weight in syllabus_weights:
            category_avg = GradeCalculator.calculate_category_average(assignments, weight.category)
            category_data = {
                'category': weight.category,
                'weight': weight.weight,
                'average': category_avg,
                'weighted_contribution': None
            }
            if category_avg is not None:
                contribution = (category_avg * weight.weight) / 100
                category_data['weighted_contribution'] = contribution
                weighted_grade += contribution
                total_weight_applied += weight.weight
            breakdown.append(category_data)
        if total_weight_applied > 0:
            final_grade = weighted_grade
            projected_final_grade = (weighted_grade / total_weight_applied) * 100 if total_weight_applied < 100 else weighted_grade
        else:
            final_grade = None
            projected_final_grade = None
        return {
            'final_grade': round(final_grade, 2) if final_grade is not None else None,
            'projected_final_grade': round(projected_final_grade, 2) if projected_final_grade is not None else None,
            'letter_grade': GradeCalculator.get_letter_grade(projected_final_grade) if projected_final_grade else None,
            'breakdown': breakdown,
            'total_weight_applied': total_weight_applied,
            'completion_percentage': round((total_weight_applied / 100) * 100, 2)
        }

    @staticmethod
    def get_letter_grade(percentage):
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
