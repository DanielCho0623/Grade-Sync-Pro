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

    SCOPES = ['https://www.googleapis.com/auth/gmail.send']

    def __init__(self):
        self.credentials_path = current_app.config.get('GMAIL_CREDENTIALS_PATH')
        self.token_path = current_app.config.get('GMAIL_TOKEN_PATH')
        self.service = None

    def authenticate(self):
        Send an email via Gmail API.

        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Email body content
            html: Whether body is HTML (default: True)

        Returns:
            Boolean indicating success
        Send a grade alert email with formatted grade information.

        Args:
            to_email: Recipient email address
            course_name: Name of the course
            grade_data: Dictionary containing grade calculation results
        <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: 
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background-color: 
                    .content {{ padding: 20px; background-color: 
                    .grade-box {{ background-color: white; border-left: 4px solid 
                    .category {{ margin: 10px 0; padding: 10px; background-color: 
                    .footer {{ text-align: center; padding: 20px; color: 
                    .warning {{ color: 
                    .success {{ color: 
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
                        <div class="category">
                            <strong>{category['category']}</strong> ({category['weight']}% of final grade)<br>
                            Average: {avg_display}
                        </div>
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
