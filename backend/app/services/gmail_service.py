import os
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from flask import current_app
import pickle

class GmailService:
    """
    Service for sending email notifications via Gmail API.
    Implements OAuth 2.0 authentication and email sending.
    """

    SCOPES = ['https://www.googleapis.com/auth/gmail.send']

    def __init__(self):
        self.credentials_path = current_app.config.get('GMAIL_CREDENTIALS_PATH')
        self.token_path = current_app.config.get('GMAIL_TOKEN_PATH')
        self.service = None

    def authenticate(self):
        """Authenticate with Gmail API using OAuth 2.0"""
        creds = None

        # Check if token file exists
        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token:
                creds = pickle.load(token)

        # If credentials are invalid or don't exist, authenticate
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            elif os.path.exists(self.credentials_path):
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, self.SCOPES)
                creds = flow.run_local_server(port=0)

                # Save credentials for future use
                os.makedirs(os.path.dirname(self.token_path), exist_ok=True)
                with open(self.token_path, 'wb') as token:
                    pickle.dump(creds, token)
            else:
                current_app.logger.error("Gmail credentials file not found")
                return False

        try:
            self.service = build('gmail', 'v1', credentials=creds)
            return True
        except Exception as e:
            current_app.logger.error(f"Gmail authentication error: {str(e)}")
            return False

    def send_email(self, to_email, subject, body, html=True):
        """
        Send an email via Gmail API.

        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Email body content
            html: Whether body is HTML (default: True)

        Returns:
            Boolean indicating success
        """
        if not self.service and not self.authenticate():
            current_app.logger.warning("Gmail service not authenticated, skipping email")
            return False

        try:
            message = MIMEMultipart('alternative')
            message['to'] = to_email
            message['subject'] = subject

            if html:
                part = MIMEText(body, 'html')
            else:
                part = MIMEText(body, 'plain')

            message.attach(part)

            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            send_message = {'raw': raw_message}

            result = self.service.users().messages().send(
                userId='me',
                body=send_message
            ).execute()

            current_app.logger.info(f"Gmail sent successfully to {to_email}: {result['id']}")
            return True

        except Exception as e:
            current_app.logger.error(f"Gmail send error: {str(e)}")
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

        # Create HTML email body
        body = f"""
        <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; }}
                    .content {{ padding: 20px; background-color: #f9f9f9; }}
                    .grade-box {{ background-color: white; border-left: 4px solid #4CAF50; padding: 15px; margin: 10px 0; }}
                    .category {{ margin: 10px 0; padding: 10px; background-color: #e8f5e9; }}
                    .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
                    .warning {{ color: #ff9800; }}
                    .success {{ color: #4CAF50; }}
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
