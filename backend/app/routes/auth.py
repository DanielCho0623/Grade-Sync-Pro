from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.models.course import Course
from app.models.assignment import Assignment
from app.models.syllabus_weight import SyllabusWeight
from app.models.grade import Grade
from app.services.brightspace_service import BrightspaceService

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password required'}), 400

    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'error': 'Email already registered'}), 400

    user = User(
        email=data['email'],
        first_name=data.get('first_name', ''),
        last_name=data.get('last_name', ''),
        brightspace_user_id=data.get('brightspace_user_id')
    )
    user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()

    _import_synthetic_courses_for_user(user.id)

    access_token = create_access_token(identity=user.id)

    return jsonify({
        'message': 'Registration successful',
        'user': user.to_dict(),
        'access_token': access_token
    }), 201

def _import_synthetic_courses_for_user(user_id):
    brightspace = BrightspaceService()
    synthetic_courses = brightspace.get_courses(user_id)

    for course_data in synthetic_courses:
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

    db.session.commit()

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password required'}), 400

    user = User.query.filter_by(email=data['email']).first()

    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401

    access_token = create_access_token(identity=user.id)

    return jsonify({
        'message': 'Login successful',
        'user': user.to_dict(),
        'access_token': access_token
    }), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({'user': user.to_dict()}), 200

@auth_bp.route('/me', methods=['PUT'])
@jwt_required()
def update_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()

    if 'first_name' in data:
        user.first_name = data['first_name']
    if 'last_name' in data:
        user.last_name = data['last_name']
    if 'brightspace_user_id' in data:
        user.brightspace_user_id = data['brightspace_user_id']
    if 'password' in data:
        user.set_password(data['password'])

    db.session.commit()

    return jsonify({
        'message': 'User updated successfully',
        'user': user.to_dict()
    }), 200
