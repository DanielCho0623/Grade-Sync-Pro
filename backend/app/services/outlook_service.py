import msal
import requests
from flask import current_app

class OutlookService:
    """
    Service for sending email notifications via Outlook/Microsoft Graph API.
    Implements OAuth 2.0 authentication and email sending.
    """

    SCOPES = ['https://graph.microsoft.com/Mail.Send']
    GRAPH_API_ENDPOINT = 'https://graph.microsoft.com/v1.0'

    def __init__(self):
        self.client_id = current_app.config.get('OUTLOOK_CLIENT_ID')
        self.client_secret = current_app.config.get('OUTLOOK_CLIENT_SECRET')
        self.tenant_id = current_app.config.get('OUTLOOK_TENANT_ID')
        self.access_token = None

    def authenticate(self):
        """Authenticate with Microsoft Graph API using OAuth 2.0"""
        if not all([self.client_id, self.client_secret, self.tenant_id]):
            current_app.logger.error("Outlook credentials not configured")
            return False

        try:
            # Create MSAL app
            authority = f'https://login.microsoftonline.com/{self.tenant_id}'
            app = msal.ConfidentialClientApplication(
                self.client_id,
                authority=authority,
                client_credential=self.client_secret
            )

            # Acquire token
            result = app.acquire_token_for_client(scopes=self.SCOPES)

            if 'access_token' in result:
                self.access_token = result['access_token']
                return True
            else:
                error = result.get('error_description', 'Unknown error')
                current_app.logger.error(f"Outlook authentication error: {error}")
                return False

        except Exception as e:
            current_app.logger.error(f"Outlook authentication error: {str(e)}")
            return False

    def send_email(self, to_email, subject, body, html=True):
        """
        Send an email via Microsoft Graph API.

        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Email body content
            html: Whether body is HTML (default: True)

        Returns:
            Boolean indicating success
        """
        if not self.access_token and not self.authenticate():
            current_app.logger.warning("Outlook service not authenticated, skipping email")
            return False

        try:
            # Prepare email message
            email_data = {
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

            # Send email
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }

            response = requests.post(
                f'{self.GRAPH_API_ENDPOINT}/me/sendMail',
                headers=headers,
                json=email_data,
                timeout=10
            )

            response.raise_for_status()
            current_app.logger.info(f"Outlook email sent successfully to {to_email}")
            return True

        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Outlook send error: {str(e)}")
            return False

    def send_grade_alert(self, to_email, course_name, grade_data):
        """
        Send a grade alert email with formatted grade information.

        Args:
            to_email: Recipient email address
            course_name: Name of the course
            grade_data: Dictionary containing grade calculation results
        """
        subject = f"GradeSync Pro: Grade Update for {course_name}"

        # Create HTML email body (same format as Gmail)
        body = f"""
        <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background-color: #0078D4; color: white; padding: 20px; text-align: center; }}
                    .content {{ padding: 20px; background-color: #f9f9f9; }}
                    .grade-box {{ background-color: white; border-left: 4px solid #0078D4; padding: 15px; margin: 10px 0; }}
                    .category {{ margin: 10px 0; padding: 10px; background-color: #E8F4FD; }}
                    .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>Grade Update Alert</h1>
                    </div>
                    <div class="content">
                        <h2>Course: {course_name}</h2>
                        <div class="grade-box">
                            <h3>Current Grade: {grade_data.get('final_grade', 'N/A')}%</h3>
                            <p>Letter Grade: <strong>{grade_data.get('letter_grade', 'N/A')}</strong></p>
                            <p>Projected Final: {grade_data.get('projected_final_grade', 'N/A')}%</p>
                            <p>Completion: {grade_data.get('completion_percentage', 'N/A')}%</p>
                        </div>

                        <h3>Grade Breakdown:</h3>
        """

        # Add category breakdown
        for category in grade_data.get('breakdown', []):
            avg = category.get('average', 'N/A')
            avg_display = f"{avg:.2f}%" if avg is not None else "No grades yet"
            body += f"""
                        <div class="category">
                            <strong>{category['category']}</strong> ({category['weight']}% of final grade)<br>
                            Average: {avg_display}
                        </div>
            """

        body += """
                        <p style="margin-top: 20px;">
                            This is an automated notification from GradeSync Pro.
                            Log in to view detailed grade information and track your progress.
                        </p>
                    </div>
                    <div class="footer">
                        <p>GradeSync Pro - Automated Grade Monitoring System</p>
                    </div>
                </div>
            </body>
        </html>
        """

        return self.send_email(to_email, subject, body, html=True)
