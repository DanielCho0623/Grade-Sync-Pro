from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from application import db
from application.models.assignment import Assignment
from application.models.grade import Grade
from application.models.course import Course

grades_bp = Blueprint('grades', __name__)

@grades_bp.route('/assignment/<int:assignment_id>', methods=['POST'])
@jwt_required()
def add_or_update_grade(assignment_id):
    user_id = int(get_jwt_identity())

    assignment = Assignment.query.join(Course).filter(
        Assignment.id == assignment_id,
        Course.user_id == user_id
    ).first()

    if not assignment:
        return jsonify({'error': 'Assignment not found'}), 404

    if not assignment.grade:
        return jsonify({'error': 'No grade found for this assignment'}), 404

    return jsonify(assignment.grade.to_dict()), 200

@grades_bp.route('/assignment/<int:assignment_id>', methods=['DELETE'])
@jwt_required()
def delete_grade(assignment_id):
    user_id = int(get_jwt_identity())

    course = Course.query.filter_by(id=course_id, user_id=user_id).first()

    if not course:
        return jsonify({'error': 'Course not found'}), 404

    grades = []
    for assignment in course.assignments:
        if assignment.grade:
            grade_data = assignment.grade.to_dict()
            grade_data['assignment_name'] = assignment.name
            grade_data['assignment_category'] = assignment.category
            grade_data['max_points'] = assignment.max_points
            grades.append(grade_data)

    return jsonify(grades), 200
