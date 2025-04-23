import os
import requests
from flask import current_app

class OutlookService:
    def __init__(self):
        self.client_id = os.getenv('OUTLOOK_CLIENT_ID', '')
        self.client_secret = os.getenv('OUTLOOK_CLIENT_SECRET', '')
        self.refresh_token = os.getenv('OUTLOOK_REFRESH_TOKEN', '')
        self.tenant_id = os.getenv('OUTLOOK_TENANT_ID', 'common')
        self.redirect_uri = os.getenv('OUTLOOK_REDIRECT_URI', 'http://localhost:5001/api/auth/outlook/callback')

        force_synthetic = os.getenv('USE_SYNTHETIC_DATA', 'true').lower() == 'true'
        self.enabled = not force_synthetic and all([self.client_id, self.client_secret, self.refresh_token])

        if not self.enabled:
            if force_synthetic:
                current_app.logger.info("Outlook: Using stub mode (forced by USE_SYNTHETIC_DATA setting)")
            else:
                current_app.logger.info("Outlook: Not configured (no OAuth credentials)")
        else:
            current_app.logger.info("Outlook: OAuth integration enabled")

    def _get_access_token(self):
        if not self.enabled:
            return None

        token_url = f'https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token'

        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token,
            'grant_type': 'refresh_token',
            'scope': 'https://graph.microsoft.com/Mail.Send offline_access'
        }

        try:
            response = requests.post(token_url, data=data)
            response.raise_for_status()
            return response.json().get('access_token')
        except Exception as e:
            current_app.logger.error(f"Outlook token refresh error: {e}")
            return None

    def _get_headers(self):
        access_token = self._get_access_token()
        if not access_token:
            return None

        return {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

    def authenticate(self):
        return self.enabled and self._get_access_token() is not None

    def send_email(self, to_email, subject, body, html=True):
        if not self.enabled:
            current_app.logger.info(f"Outlook (stub): Email to {to_email} - {subject}")
            return True

        headers = self._get_headers()
        if not headers:
            current_app.logger.error("Outlook: Failed to get access token")
            return False

        message = {
            'message': {
                'subject': subject,
                'body': {
                    'contentType': 'HTML' if html else 'Text',
                    'content': body
                },
                'toRecipients': [
                    {
                        'emailAddress': {
                            'address': to_email
                        }
                    }
                ]
            },
            'saveToSentItems': 'true'
        }

        try:
            response = requests.post(
                'https://graph.microsoft.com/v1.0/me/sendMail',
                headers=headers,
                json=message
            )
            response.raise_for_status()
            current_app.logger.info(f"Outlook: Email sent successfully to {to_email}")
            return True

        except requests.exceptions.HTTPError as error:
            current_app.logger.error(f"Outlook HTTP error: {error}")
            current_app.logger.error(f"Response: {error.response.text if hasattr(error, 'response') else 'No response'}")
            return False
        except Exception as error:
            current_app.logger.error(f"Outlook send error: {error}")
            return False

    def send_grade_alert(self, to_email, course_name, grade_data):
        subject = f"Grade Update: {course_name}"

        html_body = f"""
        <html>
            <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #0078d4; border-bottom: 2px solid #0078d4; padding-bottom: 10px;">
                        Grade Update for {course_name}
                    </h2>

                    <div style="background-color: #f3f2f1; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <h3 style="color: #323130; margin-top: 0;">Current Grade Summary</h3>
                        <p style="font-size: 18px; margin: 10px 0;">
                            <strong>Current Grade:</strong>
                            <span style="color: #107c10; font-size: 24px; font-weight: bold;">
                                {grade_data.get('current_grade', 'N/A')}%
                            </span>
                        </p>
                        <p style="font-size: 16px; margin: 10px 0;">
                            <strong>Letter Grade:</strong>
                            <span style="color: #0078d4; font-size: 20px;">
                                {grade_data.get('letter_grade', 'N/A')}
                            </span>
                        </p>
                    </div>

                    {self._build_category_breakdown_html(grade_data.get('category_breakdown', {}))}

                    <div style="margin-top: 30px; padding: 15px; background-color: #deecf9; border-left: 4px solid #0078d4; border-radius: 3px;">
                        <p style="margin: 0; font-size: 14px;">
                            <strong>Target Grade:</strong> {grade_data.get('target_grade', 85)}%<br>
                            {self._build_progress_message(grade_data)}
                        </p>
                    </div>

                    <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; text-align: center; color: #605e5c; font-size: 12px;">
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

        html = '<div style="margin: 20px 0;"><h4 style="color: #323130;">Category Breakdown</h4><table style="width: 100%; border-collapse: collapse;">'

        for category, data in categories.items():
            avg = data.get('average', 0)
            weight = data.get('weight', 0)
            html += f'''
            <tr style="border-bottom: 1px solid #edebe9;">
                <td style="padding: 10px; font-weight: bold;">{category}</td>
                <td style="padding: 10px; text-align: right;">{avg:.1f}%</td>
                <td style="padding: 10px; text-align: right; color: #605e5c;">({weight}%)</td>
            </tr>
            '''

        html += '</table></div>'
        return html

    def _build_progress_message(self, grade_data):
        current = grade_data.get('current_grade', 0)
        target = grade_data.get('target_grade', 85)

        if current >= target:
            return f'<span style="color: #107c10;">You are meeting your target grade!</span>'
        else:
            diff = target - current
            return f'<span style="color: #d83b01;">You need {diff:.1f}% more to reach your target.</span>'

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
