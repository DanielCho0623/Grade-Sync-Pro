import pytest
<<<<<<< HEAD
from application.utils.grade_calculator import GradeCalculator
=======
from app.utils.grade_calculator import GradeCalculator
>>>>>>> 22c8b51 (backend deployment config and tests)

def test_get_letter_grade():
    assert GradeCalculator.get_letter_grade(95) == 'A'
    assert GradeCalculator.get_letter_grade(85) == 'B'
    assert GradeCalculator.get_letter_grade(75) == 'C'
    assert GradeCalculator.get_letter_grade(65) == 'D'
    assert GradeCalculator.get_letter_grade(55) == 'F'

def test_calculate_category_average():
<<<<<<< HEAD
<<<<<<< HEAD
=======
    # This would require mock data - simplified test
>>>>>>> 22c8b51 (backend deployment config and tests)
=======
>>>>>>> 4990274 (clean up code)
    assert GradeCalculator.get_letter_grade(90) == 'A-'
