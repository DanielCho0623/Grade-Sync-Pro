from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.notification import Notification
from app.models.course import Course
from app.models.user import User
from app.services.gmail_service import GmailService
from app.services.outlook_service import OutlookService
from app.utils.grade_calculator import GradeCalculator

notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.route('/', methods=['GET'])
@jwt_required()
def get_notifications():
    user_id = int(get_jwt_identity())
    notifications = Notification.query.filter_by(user_id=user_id).order_by(
        Notification.created_at.desc()
    ).all()

    return jsonify({
        'notifications': [n.to_dict() for n in notifications]
    }), 200

@notifications_bp.route('/<int:notification_id>/read', methods=['PUT'])
@jwt_required()
def mark_as_read(notification_id):
    user_id = int(get_jwt_identity())
    notification = Notification.query.filter_by(
        id=notification_id,
        user_id=user_id
    ).first()

    if not notification:
        return jsonify({'error': 'Notification not found'}), 404

    notification.is_read = True
    db.session.commit()

    return jsonify({
        'message': 'Notification marked as read',
        'notification': notification.to_dict()
    }), 200

@notifications_bp.route('/send-grade-alert/<int:course_id>', methods=['POST'])
@jwt_required()
def send_grade_alert(course_id):
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    course = Course.query.filter_by(id=course_id, user_id=user_id).first()

    if not course:
        return jsonify({'error': 'Course not found'}), 404

    grade_data = GradeCalculator.calculate_course_grade(course)

    if grade_data.get('error'):
        return jsonify({'error': grade_data['error']}), 400

    data = request.get_json() or {}
    use_gmail = data.get('use_gmail', True)
    use_outlook = data.get('use_outlook', True)
    recipient_email = data.get('email', current_app.config.get('ALERT_EMAIL') or user.email)

    sent_via = []

    if use_gmail:
        try:
            gmail_service = GmailService()
            if gmail_service.send_grade_alert(recipient_email, course.course_name, grade_data):
                sent_via.append('gmail')
        except Exception as e:
            current_app.logger.error(f"Gmail notification error: {str(e)}")

    if use_outlook:
        try:
            outlook_service = OutlookService()
            if outlook_service.send_grade_alert(recipient_email, course.course_name, grade_data):
                sent_via.append('outlook')
        except Exception as e:
            current_app.logger.error(f"Outlook notification error: {str(e)}")

    if not sent_via:
        return jsonify({
            'error': 'Failed to send notification via any service',
            'message': 'Check email service configuration'
        }), 500

    notification = Notification(
        user_id=user_id,
        notification_type='grade_alert',
        subject=f'Grade Update for {course.course_name}',
        message=f"Current grade: {grade_data.get('final_grade', 'N/A')}% ({grade_data.get('letter_grade', 'N/A')})",
        sent_via=', '.join(sent_via)
    )
    db.session.add(notification)
    db.session.commit()

    return jsonify({
        'message': 'Grade alert sent successfully',
        'sent_via': sent_via,
        'grade_data': grade_data,
        'notification': notification.to_dict()
    }), 200

@notifications_bp.route('/auto-check', methods=['POST'])
@jwt_required()
def auto_check_grades():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    courses = Course.query.filter_by(user_id=user_id).all()

    threshold = current_app.config.get('GRADE_THRESHOLD', 85.0)
    alerts_sent = []

    for course in courses:
        grade_data = GradeCalculator.calculate_course_grade(course)

        if grade_data.get('error'):
            continue

        projected_grade = grade_data.get('projected_final_grade')

        if projected_grade and (projected_grade < threshold or projected_grade < course.target_grade):
            gmail_service = GmailService()
            outlook_service = OutlookService()

            sent_via = []

            try:
                if gmail_service.send_grade_alert(user.email, course.course_name, grade_data):
                    sent_via.append('gmail')
            except Exception as e:
                current_app.logger.error(f"Gmail error for {course.course_name}: {str(e)}")

            try:
                if outlook_service.send_grade_alert(user.email, course.course_name, grade_data):
                    sent_via.append('outlook')
            except Exception as e:
                current_app.logger.error(f"Outlook error for {course.course_name}: {str(e)}")

            if sent_via:
                notification = Notification(
                    user_id=user_id,
                    notification_type='grade_alert',
                    subject=f'Grade Alert: {course.course_name}',
                    message=f"Grade {projected_grade}% is below target {course.target_grade}%",
                    sent_via=', '.join(sent_via)
                )
                db.session.add(notification)

                alerts_sent.append({
                    'course': course.course_name,
                    'grade': projected_grade,
                    'target': course.target_grade,
                    'sent_via': sent_via
                })

    db.session.commit()

    return jsonify({
        'message': f'Checked {len(courses)} courses, sent {len(alerts_sent)} alerts',
        'alerts': alerts_sent
    }), 200
