import os
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GmailService:
    def __init__(self):
        self.client_id = os.getenv('GMAIL_CLIENT_ID', '')
        self.client_secret = os.getenv('GMAIL_CLIENT_SECRET', '')
        self.refresh_token = os.getenv('GMAIL_REFRESH_TOKEN', '')
        self.redirect_uri = os.getenv('GMAIL_REDIRECT_URI', 'http://localhost:5001/api/auth/gmail/callback')

        force_synthetic = os.getenv('USE_SYNTHETIC_DATA', 'true').lower() == 'true'
        self.enabled = not force_synthetic and all([self.client_id, self.client_secret, self.refresh_token])

        try:
            if not self.enabled:
                if force_synthetic:
                    current_app.logger.info("Gmail: Using stub mode (forced by USE_SYNTHETIC_DATA setting)")
                else:
                    current_app.logger.info("Gmail: Not configured (no OAuth credentials)")
            else:
                current_app.logger.info("Gmail: OAuth integration enabled")
        except RuntimeError:
            pass

    def _get_credentials(self):
        if not self.enabled:
            return None

        creds = Credentials(
            None,
            refresh_token=self.refresh_token,
            token_uri='https://oauth2.googleapis.com/token',
            client_id=self.client_id,
            client_secret=self.client_secret
        )

        if creds.expired:
            creds.refresh(Request())

        return creds

    def _build_service(self):
        try:
            creds = self._get_credentials()
            if not creds:
                return None
            return build('gmail', 'v1', credentials=creds)
        except Exception as e:
            current_app.logger.error(f"Gmail service build error: {e}")
            return None

    def authenticate(self):
        return self.enabled and self._build_service() is not None

    def send_email(self, to_email, subject, body, html=True):
        if not self.enabled:
            current_app.logger.info(f"Gmail (stub): Email to {to_email} - {subject}")
            return True

        try:
            service = self._build_service()
            if not service:
                current_app.logger.error("Gmail: Failed to build service")
                return False

            message = MIMEMultipart('alternative')
            message['To'] = to_email
            message['Subject'] = subject

            if html:
                part = MIMEText(body, 'html')
            else:
                part = MIMEText(body, 'plain')

            message.attach(part)

            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            send_message = {'raw': raw_message}

            result = service.users().messages().send(userId='me', body=send_message).execute()
            current_app.logger.info(f"Gmail: Email sent successfully (ID: {result.get('id')})")
            return True

        except HttpError as error:
            current_app.logger.error(f"Gmail HTTP error: {error}")
            return False
        except Exception as error:
            current_app.logger.error(f"Gmail send error: {error}")
            return False

    def send_grade_alert(self, to_email, course_name, grade_data):
        subject = f"Grade Update: {course_name}"

        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px;">
                        Grade Update for {course_name}
                    </h2>

                    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <h3 style="color: #2c3e50; margin-top: 0;">Current Grade Summary</h3>
                        <p style="font-size: 18px; margin: 10px 0;">
                            <strong>Current Grade:</strong>
                            <span style="color: #27ae60; font-size: 24px; font-weight: bold;">
                                {grade_data.get('current_grade', 'N/A')}%
                            </span>
                        </p>
                        <p style="font-size: 16px; margin: 10px 0;">
                            <strong>Letter Grade:</strong>
                            <span style="color: #2980b9; font-size: 20px;">
                                {grade_data.get('letter_grade', 'N/A')}
                            </span>
                        </p>
                    </div>

                    {self._build_category_breakdown_html(grade_data.get('category_breakdown', {}))}

                    <div style="margin-top: 30px; padding: 15px; background-color: #e8f4f8; border-left: 4px solid #3498db; border-radius: 3px;">
                        <p style="margin: 0; font-size: 14px;">
                            <strong>Target Grade:</strong> {grade_data.get('target_grade', 85)}%<br>
                            {self._build_progress_message(grade_data)}
                        </p>
                    </div>

                    <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; text-align: center; color: #7f8c8d; font-size: 12px;">
                        <p>This is an automated notification from GradeSync Pro</p>
                    </div>
                </div>
            </body>
        </html>
        """

        return self.send_email(to_email, subject, html_body, html=True)

    def _build_category_breakdown_html(self, categories):
        if not categories:
            return ''

        html = '<div style="margin: 20px 0;"><h4 style="color: #2c3e50;">Category Breakdown</h4><table style="width: 100%; border-collapse: collapse;">'

        for category, data in categories.items():
            avg = data.get('average', 0)
            weight = data.get('weight', 0)
            html += f'''
            <tr style="border-bottom: 1px solid #ddd;">
                <td style="padding: 10px; font-weight: bold;">{category}</td>
                <td style="padding: 10px; text-align: right;">{avg:.1f}%</td>
                <td style="padding: 10px; text-align: right; color: #7f8c8d;">({weight}%)</td>
            </tr>
            '''

        html += '</table></div>'
        return html

    def _build_progress_message(self, grade_data):
        current = grade_data.get('current_grade', 0)
        target = grade_data.get('target_grade', 85)

        if current >= target:
            return f'<span style="color: #27ae60;">You are meeting your target grade!</span>'
        else:
            diff = target - current
            return f'<span style="color: #e67e22;">You need {diff:.1f}% more to reach your target.</span>'

    def send_batch_alerts(self, alerts):
        results = []
        for alert in alerts:
            success = self.send_grade_alert(
                alert['email'],
                alert['course_name'],
                alert['grade_data']
            )
            results.append({'email': alert['email'], 'success': success})

        return results
