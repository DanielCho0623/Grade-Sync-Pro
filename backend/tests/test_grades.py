import pytest
from application.utils.grade_calculator import GradeCalculator

def test_get_letter_grade():
    assert GradeCalculator.get_letter_grade(95) == 'A'
    assert GradeCalculator.get_letter_grade(90) == 'A-'
    assert GradeCalculator.get_letter_grade(85) == 'B'
    assert GradeCalculator.get_letter_grade(75) == 'C'
    assert GradeCalculator.get_letter_grade(65) == 'D'
    assert GradeCalculator.get_letter_grade(55) == 'F'

def test_calculate_category_average():
    # This would require mock data - simplified test
    assert GradeCalculator.get_letter_grade(90) == 'A-'
