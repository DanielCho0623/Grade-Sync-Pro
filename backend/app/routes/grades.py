from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.assignment import Assignment
from app.models.grade import Grade
from app.models.course import Course

grades_bp = Blueprint('grades', __name__)

@grades_bp.route('/assignment/<int:assignment_id>', methods=['POST'])
@jwt_required()
def add_or_update_grade(assignment_id):
    """Add or update a grade for an assignment"""
    user_id = get_jwt_identity()

    # Verify assignment belongs to user's course
    assignment = Assignment.query.join(Course).filter(
        Assignment.id == assignment_id,
        Course.user_id == user_id
    ).first()

    if not assignment:
        return jsonify({'error': 'Assignment not found'}), 404

    data = request.get_json()

    if data.get('points_earned') is None:
        return jsonify({'error': 'points_earned is required'}), 400

    # Check if grade already exists
    grade = assignment.grade

    if grade:
        # Update existing grade
        grade.points_earned = data['points_earned']
        grade.percentage = (data['points_earned'] / assignment.max_points) * 100
        grade.letter_grade = data.get('letter_grade')
        grade.feedback = data.get('feedback')
        grade.graded_date = data.get('graded_date')
    else:
        # Create new grade
        grade = Grade(
            assignment_id=assignment_id,
            points_earned=data['points_earned'],
            percentage=(data['points_earned'] / assignment.max_points) * 100,
            letter_grade=data.get('letter_grade'),
            feedback=data.get('feedback'),
            graded_date=data.get('graded_date')
        )
        db.session.add(grade)

    db.session.commit()

    return jsonify({
        'message': 'Grade saved successfully',
        'grade': grade.to_dict()
    }), 201

@grades_bp.route('/assignment/<int:assignment_id>', methods=['GET'])
@jwt_required()
def get_grade(assignment_id):
    """Get grade for a specific assignment"""
    user_id = get_jwt_identity()

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
    """Delete a grade"""
    user_id = get_jwt_identity()

    assignment = Assignment.query.join(Course).filter(
        Assignment.id == assignment_id,
        Course.user_id == user_id
    ).first()

    if not assignment:
        return jsonify({'error': 'Assignment not found'}), 404

    if not assignment.grade:
        return jsonify({'error': 'No grade found for this assignment'}), 404

    db.session.delete(assignment.grade)
    db.session.commit()

    return jsonify({'message': 'Grade deleted successfully'}), 200

@grades_bp.route('/course/<int:course_id>', methods=['GET'])
@jwt_required()
def get_course_grades(course_id):
    """Get all grades for a course"""
    user_id = get_jwt_identity()

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
