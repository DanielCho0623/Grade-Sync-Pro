from flask import current_app

class GmailService:
    def __init__(self):
        pass

    def authenticate(self):
        return False

    def send_email(self, to_email, subject, body, html=True):
        current_app.logger.info(f"Email would be sent to: {to_email}")
        return True

    def send_grade_alert(self, to_email, course_name, grade_data):
        return self.send_email(to_email, f"Grade Alert: {course_name}", "Grade update")
