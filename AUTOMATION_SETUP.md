# Automation Setup Guide

This guide explains how to enable the full automation features for GradeSync Pro, including Brightspace integration and email notifications via Gmail or Outlook.

## Current Status

The automation features are **fully implemented** and ready to use. Currently running in development mode with synthetic data because API credentials are not configured.

## Features Available

1. **Brightspace Integration**: Automatically sync courses, assignments, and grades from your school's Brightspace/D2L system
2. **Gmail Notifications**: Send automated grade alerts via Gmail with OAuth 2.0
3. **Outlook Notifications**: Send automated grade alerts via Microsoft Outlook/Office 365

## Quick Start

The app works in **hybrid mode**:
- Without API credentials: Uses synthetic test data (current mode)
- With API credentials: Connects to real Brightspace and email services

You can use the app immediately with test data, or follow the setup instructions below to enable real integrations.

---

## Option 1: Gmail Integration Setup

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the **Gmail API**:
   - Go to "APIs & Services" > "Library"
   - Search for "Gmail API"
   - Click "Enable"

### Step 2: Create OAuth 2.0 Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. Configure OAuth consent screen if prompted:
   - User Type: External
   - App name: GradeSync Pro
   - User support email: Your email
   - Developer contact: Your email
4. Application type: Web application
5. Authorized redirect URIs: `http://localhost:5001/api/auth/gmail/callback`
6. Click "Create"
7. Save the **Client ID** and **Client Secret**

### Step 3: Get Refresh Token

Run this Python script to get your refresh token:

```python
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

flow = InstalledAppFlow.from_client_secrets_file(
    'credentials.json',  # Download from Google Cloud Console
    SCOPES
)

creds = flow.run_local_server(port=0)
print(f"Refresh Token: {creds.refresh_token}")
```

### Step 4: Add to .env File

```bash
GMAIL_CLIENT_ID=your_client_id_here
GMAIL_CLIENT_SECRET=your_client_secret_here
GMAIL_REFRESH_TOKEN=your_refresh_token_here
GMAIL_REDIRECT_URI=http://localhost:5001/api/auth/gmail/callback
```

---

## Option 2: Outlook/Office 365 Integration Setup

### Step 1: Register Application in Azure

1. Go to [Azure Portal](https://portal.azure.com/)
2. Navigate to "Azure Active Directory" > "App registrations"
3. Click "New registration"
4. Name: GradeSync Pro
5. Supported account types: "Accounts in any organizational directory and personal Microsoft accounts"
6. Redirect URI: Web > `http://localhost:5001/api/auth/outlook/callback`
7. Click "Register"

### Step 2: Configure API Permissions

1. Go to "API permissions"
2. Click "Add a permission"
3. Select "Microsoft Graph"
4. Select "Delegated permissions"
5. Add these permissions:
   - Mail.Send
   - offline_access
6. Click "Grant admin consent"

### Step 3: Create Client Secret

1. Go to "Certificates & secrets"
2. Click "New client secret"
3. Description: GradeSync Pro
4. Expires: 24 months
5. Click "Add"
6. **Copy the secret value immediately** (you won't see it again)

### Step 4: Get Refresh Token

Use this URL (replace YOUR_CLIENT_ID):

```
https://login.microsoftonline.com/common/oauth2/v2.0/authorize?
client_id=YOUR_CLIENT_ID
&response_type=code
&redirect_uri=http://localhost:5001/api/auth/outlook/callback
&response_mode=query
&scope=https://graph.microsoft.com/Mail.Send offline_access
```

After authorization, exchange the code for tokens using:

```bash
curl -X POST https://login.microsoftonline.com/common/oauth2/v2.0/token \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET" \
  -d "code=AUTHORIZATION_CODE" \
  -d "redirect_uri=http://localhost:5001/api/auth/outlook/callback" \
  -d "grant_type=authorization_code"
```

### Step 5: Add to .env File

```bash
OUTLOOK_CLIENT_ID=your_application_id_here
OUTLOOK_CLIENT_SECRET=your_client_secret_here
OUTLOOK_REFRESH_TOKEN=your_refresh_token_here
OUTLOOK_TENANT_ID=common
OUTLOOK_REDIRECT_URI=http://localhost:5001/api/auth/outlook/callback
```

---

## Option 3: Brightspace/D2L Integration Setup

### Step 1: Get Brightspace Credentials

Contact your school's IT department or LMS administrator to get:
- Brightspace Base URL (e.g., `https://yourschool.brightspace.com`)
- API App ID
- API App Key
- User ID
- User Key

### Step 2: Add to .env File

```bash
BRIGHTSPACE_BASE_URL=https://yourschool.brightspace.com
BRIGHTSPACE_APP_ID=your_app_id_here
BRIGHTSPACE_APP_KEY=your_app_key_here
BRIGHTSPACE_USER_ID=your_user_id_here
BRIGHTSPACE_USER_KEY=your_user_key_here
```

---

## Testing the Setup

### 1. Restart the Backend Server

After updating the `.env` file:

```bash
cd backend
python3 run.py
```

Check the logs for:
- `Brightspace: Real API integration enabled` (if configured)
- `Gmail: OAuth integration enabled` (if configured)
- `Outlook: OAuth integration enabled` (if configured)

### 2. Test Brightspace Sync

In the frontend:
1. Click on a course
2. Click "Sync from Brightspace"
3. Assignments and grades will automatically sync

### 3. Test Email Notifications

In the frontend:
1. Go to Settings or Notifications
2. Click "Send Test Email"
3. Check your email inbox

---

## Development Mode (No API Credentials)

The app works perfectly without any API credentials:

**Brightspace**: Generates realistic synthetic courses, assignments, and grades
**Email Services**: Logs email details to console instead of sending

This is perfect for:
- Local development
- Testing the UI
- Demonstrating the app
- Development without access to real APIs

---

## Production Deployment

For Railway deployment, add all environment variables in the Railway dashboard:
1. Go to your Railway project
2. Click on your backend service
3. Go to "Variables" tab
4. Add all the environment variables from your `.env` file

---

## Troubleshooting

### Gmail Issues

**Error**: "Invalid grant"
- Your refresh token expired
- Generate a new refresh token following Step 3

**Error**: "Insufficient permissions"
- Make sure Gmail API is enabled
- Verify OAuth consent screen is configured

### Outlook Issues

**Error**: "Invalid client"
- Check your CLIENT_ID and CLIENT_SECRET
- Verify redirect URI matches Azure configuration

**Error**: "Token refresh failed"
- Your refresh token may have expired
- Re-authorize and get a new refresh token

### Brightspace Issues

**Error**: "Authentication failed"
- Verify your API credentials with IT department
- Check that BASE_URL is correct

---

## Need Help?

Check the backend logs for detailed error messages:
```bash
cd backend
tail -f app.log  # if logging to file
# or check the terminal output
```

The services will automatically fall back to synthetic mode if there are configuration issues, so the app will always work.
