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

    assignment = Assignment.query.join(Course).filter(
        Assignment.id == assignment_id,
        Course.user_id == user_id
    ).first()

    if not assignment:
        return jsonify({'error': 'Assignment not found'}), 404

    if not assignment.grade:
        return jsonify({'error': 'No grade to delete'}), 404

    db.session.delete(assignment.grade)
    db.session.commit()

    return jsonify({'message': 'Grade deleted successfully'}), 200
