from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.course import Course
from app.models.assignment import Assignment
from app.models.syllabus_weight import SyllabusWeight
from app.models.grade import Grade
from app.utils.grade_calculator import GradeCalculator
from app.services.brightspace_service import BrightspaceService

courses_bp = Blueprint('courses', __name__)

@courses_bp.route('/', methods=['GET'])
@jwt_required()
def get_courses():
    user_id = int(get_jwt_identity())
    courses = Course.query.filter_by(user_id=user_id).all()

    return jsonify({
        'courses': [course.to_dict() for course in courses]
    }), 200

@courses_bp.route('/import-synthetic', methods=['POST'])
@jwt_required()
def import_synthetic_courses():
    user_id = int(get_jwt_identity())

    brightspace = BrightspaceService()
    synthetic_courses = brightspace.get_courses(user_id)

    imported_courses = []

    for course_data in synthetic_courses:
        existing = Course.query.filter_by(
            user_id=user_id,
            brightspace_course_id=course_data['brightspace_course_id']
        ).first()

        if existing:
            continue

        course = Course(
            user_id=user_id,
            brightspace_course_id=course_data['brightspace_course_id'],
            course_code=course_data['course_code'],
            course_name=course_data['course_name'],
            semester=course_data.get('semester'),
            year=course_data.get('year'),
            target_grade=85.0
        )

        db.session.add(course)
        db.session.flush()

        assignments_data = brightspace.get_assignments(course_data['brightspace_course_id'])

        for assignment_data in assignments_data:
            assignment = Assignment(
                course_id=course.id,
                brightspace_assignment_id=assignment_data['brightspace_assignment_id'],
                name=assignment_data['name'],
                category=assignment_data['category'],
                max_points=assignment_data['max_points'],
                due_date=assignment_data.get('due_date'),
                description=assignment_data.get('description')
            )
            db.session.add(assignment)
            db.session.flush()

        grades_data = brightspace.get_grades(course_data['brightspace_course_id'], user_id)

        for assignment_id, grade_data in grades_data.items():
            assignment = Assignment.query.filter_by(
                course_id=course.id,
                brightspace_assignment_id=assignment_id
            ).first()

            if assignment:
                grade = Grade(
                    assignment_id=assignment.id,
                    points_earned=grade_data['points_earned'],
                    percentage=(grade_data['points_earned'] / assignment.max_points) * 100,
                    graded_date=grade_data.get('graded_date'),
                    feedback=grade_data.get('feedback')
                )
                db.session.add(grade)

        weights = [
            {'category': 'Homework', 'weight': 30.0, 'description': 'Weekly homework assignments'},
            {'category': 'Quiz', 'weight': 20.0, 'description': 'In-class quizzes'},
            {'category': 'Exam', 'weight': 40.0, 'description': 'Midterm and final exams'},
            {'category': 'Project', 'weight': 10.0, 'description': 'Course project'}
        ]

        for weight_data in weights:
            weight = SyllabusWeight(
                course_id=course.id,
                category=weight_data['category'],
                weight=weight_data['weight'],
                description=weight_data['description']
            )
            db.session.add(weight)

        imported_courses.append(course)

    db.session.commit()

    return jsonify({
        'message': f'Imported {len(imported_courses)} synthetic courses',
        'courses': [course.to_dict(include_assignments=True, include_weights=True) for course in imported_courses]
    }), 200

@courses_bp.route('/', methods=['POST'])
@jwt_required()
def create_course():
    user_id = int(get_jwt_identity())
    data = request.get_json()

    if not data.get('course_code') or not data.get('course_name'):
        return jsonify({'error': 'Course code and name are required'}), 400

    course = Course(
        user_id=user_id,
        course_code=data['course_code'],
        course_name=data['course_name'],
        semester=data.get('semester'),
        year=data.get('year'),
        brightspace_course_id=data.get('brightspace_course_id'),
        target_grade=data.get('target_grade', 85.0)
    )

    db.session.add(course)
    db.session.commit()

    return jsonify({
        'message': 'Course created successfully',
        'course': course.to_dict()
    }), 201

@courses_bp.route('/<int:course_id>', methods=['GET'])
@jwt_required()
def get_course(course_id):
    user_id = int(get_jwt_identity())
    course = Course.query.filter_by(id=course_id, user_id=user_id).first()

    if not course:
        return jsonify({'error': 'Course not found'}), 404

    return jsonify({
        'course': course.to_dict(include_assignments=True, include_weights=True)
    }), 200

@courses_bp.route('/<int:course_id>', methods=['PUT'])
@jwt_required()
def update_course(course_id):
    user_id = int(get_jwt_identity())
    course = Course.query.filter_by(id=course_id, user_id=user_id).first()

    if not course:
        return jsonify({'error': 'Course not found'}), 404

    data = request.get_json()

    if 'course_code' in data:
        course.course_code = data['course_code']
    if 'course_name' in data:
        course.course_name = data['course_name']
    if 'semester' in data:
        course.semester = data['semester']
    if 'year' in data:
        course.year = data['year']
    if 'target_grade' in data:
        course.target_grade = data['target_grade']

    db.session.commit()

    return jsonify({
        'message': 'Course updated successfully',
        'course': course.to_dict()
    }), 200

@courses_bp.route('/<int:course_id>', methods=['DELETE'])
@jwt_required()
def delete_course(course_id):
    user_id = int(get_jwt_identity())
    course = Course.query.filter_by(id=course_id, user_id=user_id).first()

    if not course:
        return jsonify({'error': 'Course not found'}), 404

    db.session.delete(course)
    db.session.commit()

    return jsonify({'message': 'Course deleted successfully'}), 200

@courses_bp.route('/<int:course_id>/sync', methods=['POST'])
@jwt_required()
def sync_course(course_id):
    user_id = int(get_jwt_identity())
    course = Course.query.filter_by(id=course_id, user_id=user_id).first()

    if not course:
        return jsonify({'error': 'Course not found'}), 404

    brightspace = BrightspaceService()

    assignments_data = brightspace.get_assignments(course.brightspace_course_id or course_id)

    synced_count = 0
    for assignment_data in assignments_data:
        assignment = Assignment.query.filter_by(
            course_id=course_id,
            brightspace_assignment_id=assignment_data.get('brightspace_assignment_id')
        ).first()

        if not assignment:
            assignment = Assignment(
                course_id=course_id,
                brightspace_assignment_id=assignment_data.get('brightspace_assignment_id'),
                name=assignment_data['name'],
                category=assignment_data.get('category', 'Homework'),
                max_points=assignment_data['max_points'],
                due_date=assignment_data.get('due_date'),
                description=assignment_data.get('description')
            )
            db.session.add(assignment)
            synced_count += 1

    grades_data = brightspace.get_grades(course.brightspace_course_id or course_id, user_id)

    for assignment_id, grade_data in grades_data.items():
        assignment = Assignment.query.filter_by(
            course_id=course_id,
            brightspace_assignment_id=assignment_id
        ).first()

        if assignment:
            grade = assignment.grade or Grade(assignment_id=assignment.id)
            grade.points_earned = grade_data.get('points_earned')
            grade.percentage = (grade_data.get('points_earned') / assignment.max_points) * 100
            grade.graded_date = grade_data.get('graded_date')
            grade.feedback = grade_data.get('feedback')

            if not assignment.grade:
                db.session.add(grade)

    db.session.commit()

    return jsonify({
        'message': f'Synced {synced_count} assignments from Brightspace',
        'course': course.to_dict(include_assignments=True)
    }), 200

@courses_bp.route('/<int:course_id>/calculate', methods=['GET'])
@jwt_required()
def calculate_course_grade(course_id):
    user_id = int(get_jwt_identity())
    course = Course.query.filter_by(id=course_id, user_id=user_id).first()

    if not course:
        return jsonify({'error': 'Course not found'}), 404

    grade_data = GradeCalculator.calculate_course_grade(course)

    return jsonify(grade_data), 200

@courses_bp.route('/<int:course_id>/grade-needed', methods=['GET'])
@jwt_required()
def calculate_grade_needed(course_id):
    user_id = int(get_jwt_identity())
    course = Course.query.filter_by(id=course_id, user_id=user_id).first()

    if not course:
        return jsonify({'error': 'Course not found'}), 404

    target_grade = request.args.get('target', course.target_grade, type=float)
    needed_data = GradeCalculator.calculate_grade_needed(course, target_grade)

    return jsonify(needed_data), 200

@courses_bp.route('/<int:course_id>/weights', methods=['POST'])
@jwt_required()
def add_syllabus_weight(course_id):
    user_id = int(get_jwt_identity())
    course = Course.query.filter_by(id=course_id, user_id=user_id).first()

    if not course:
        return jsonify({'error': 'Course not found'}), 404

    data = request.get_json()

    if not data.get('category') or data.get('weight') is None:
        return jsonify({'error': 'Category and weight are required'}), 400

    weight = SyllabusWeight.query.filter_by(
        course_id=course_id,
        category=data['category']
    ).first()

    if weight:
        weight.weight = data['weight']
        weight.description = data.get('description')
    else:
        weight = SyllabusWeight(
            course_id=course_id,
            category=data['category'],
            weight=data['weight'],
            description=data.get('description')
        )
        db.session.add(weight)

    db.session.commit()

    return jsonify({
        'message': 'Syllabus weight saved successfully',
        'weight': weight.to_dict()
    }), 201

@courses_bp.route('/<int:course_id>/weights/<int:weight_id>', methods=['DELETE'])
@jwt_required()
def delete_syllabus_weight(course_id, weight_id):
    user_id = int(get_jwt_identity())
    course = Course.query.filter_by(id=course_id, user_id=user_id).first()

    if not course:
        return jsonify({'error': 'Course not found'}), 404

    weight = SyllabusWeight.query.filter_by(id=weight_id, course_id=course_id).first()

    if not weight:
        return jsonify({'error': 'Weight not found'}), 404

    db.session.delete(weight)
    db.session.commit()

    return jsonify({'message': 'Weight deleted successfully'}), 200

@courses_bp.route('/<int:course_id>/assignments', methods=['POST'])
@jwt_required()
def add_assignment(course_id):
    user_id = int(get_jwt_identity())
    course = Course.query.filter_by(id=course_id, user_id=user_id).first()

    if not course:
        return jsonify({'error': 'Course not found'}), 404

    data = request.get_json()

    if not data.get('name') or data.get('max_points') is None:
        return jsonify({'error': 'Name and max_points are required'}), 400

    assignment = Assignment(
        course_id=course_id,
        name=data['name'],
        category=data.get('category', 'Homework'),
        max_points=data['max_points'],
        due_date=data.get('due_date'),
        description=data.get('description'),
        brightspace_assignment_id=data.get('brightspace_assignment_id')
    )

    db.session.add(assignment)
    db.session.commit()

    return jsonify({
        'message': 'Assignment added successfully',
        'assignment': assignment.to_dict()
    }), 201

@courses_bp.route('/<int:course_id>/assignments/<int:assignment_id>', methods=['DELETE'])
@jwt_required()
def delete_assignment(course_id, assignment_id):
    user_id = int(get_jwt_identity())
    course = Course.query.filter_by(id=course_id, user_id=user_id).first()

    if not course:
        return jsonify({'error': 'Course not found'}), 404

    assignment = Assignment.query.filter_by(id=assignment_id, course_id=course_id).first()

    if not assignment:
        return jsonify({'error': 'Assignment not found'}), 404

    db.session.delete(assignment)
    db.session.commit()

    return jsonify({'message': 'Assignment deleted successfully'}), 200
