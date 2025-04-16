# GradeSync Pro - Complete Setup Guide

This guide will walk you through setting up GradeSync Pro from scratch.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Database Setup](#database-setup)
3. [Backend Setup](#backend-setup)
4. [Frontend Setup](#frontend-setup)
5. [Email Integration](#email-integration)
6. [Brightspace Integration](#brightspace-integration)
7. [Deployment](#deployment)

## Prerequisites

Install the following on your system:

1. **Python 3.11+**
   - Download from [python.org](https://www.python.org/downloads/)
   - Verify: `python --version`

2. **Node.js 18+**
   - Download from [nodejs.org](https://nodejs.org/)
   - Verify: `node --version` and `npm --version`

3. **PostgreSQL 15+**
   - Download from [postgresql.org](https://www.postgresql.org/download/)
   - Verify: `psql --version`

4. **Git**
   - Download from [git-scm.com](https://git-scm.com/)
   - Verify: `git --version`

## Database Setup

1. **Start PostgreSQL**
   ```bash
   # On macOS with Homebrew
   brew services start postgresql@15

   # On Linux
   sudo systemctl start postgresql

   # On Windows
   # Use pg_ctl or Services
   ```

2. **Create Database**
   ```bash
   psql postgres
   ```

   In PostgreSQL shell:
   ```sql
   CREATE DATABASE gradesync;
   CREATE USER gradesync_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE gradesync TO gradesync_user;
   \q
   ```

3. **Note your connection string**
   ```
   postgresql://gradesync_user:your_password@localhost:5432/gradesync
   ```

## Backend Setup

1. **Clone and navigate to backend**
   ```bash
   cd GradeSync-Pro/backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv

   # Activate
   # macOS/Linux:
   source venv/bin/activate

   # Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   ```

   Edit `.env`:
   ```
   FLASK_APP=app
   FLASK_ENV=development
   SECRET_KEY=generate-a-random-secret-key-here
   JWT_SECRET_KEY=generate-another-random-key-here
   DATABASE_URL=postgresql://gradesync_user:your_password@localhost:5432/gradesync
   ```

5. **Initialize database**
   ```bash
   python
   ```

   In Python shell:
   ```python
   from app import create_app, db
   app = create_app()
   with app.app_context():
       db.create_all()
   exit()
   ```

6. **Run backend server**
   ```bash
   python app.py
   ```

   Server should start at `http://localhost:5000`

## Frontend Setup

1. **Navigate to frontend**
   ```bash
   cd ../frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   ```

   Edit `.env`:
   ```
   REACT_APP_API_URL=http://localhost:5000/api
   ```

4. **Run frontend server**
   ```bash
   npm start
   ```

   Application should open at `http://localhost:3000`

## Email Integration

### Gmail Setup

1. **Google Cloud Console**
   - Go to [console.cloud.google.com](https://console.cloud.google.com)
   - Create a new project "GradeSync Pro"

2. **Enable Gmail API**
   - Navigate to "APIs & Services" > "Library"
   - Search for "Gmail API"
   - Click "Enable"

3. **Create Credentials**
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Application type: "Desktop app"
   - Name: "GradeSync Pro Gmail"
   - Download JSON credentials

4. **Configure Backend**
   - Create `backend/credentials` directory
   - Save downloaded file as `backend/credentials/gmail_credentials.json`
   - Update `.env`:
     ```
     GMAIL_CREDENTIALS_PATH=credentials/gmail_credentials.json
     GMAIL_TOKEN_PATH=credentials/gmail_token.json
     ```

5. **First Run Authentication**
   - First email send will open browser for OAuth
   - Authorize the application
   - Token saved for future use

### Outlook Setup

1. **Azure Portal**
   - Go to [portal.azure.com](https://portal.azure.com)
   - Navigate to "Azure Active Directory" > "App registrations"

2. **Register Application**
   - Click "New registration"
   - Name: "GradeSync Pro"
   - Supported account types: "Accounts in any organizational directory"
   - Click "Register"

3. **Configure API Permissions**
   - Go to "API permissions"
   - Click "Add a permission"
   - Select "Microsoft Graph" > "Application permissions"
   - Add "Mail.Send"
   - Click "Grant admin consent"

4. **Create Client Secret**
   - Go to "Certificates & secrets"
   - Click "New client secret"
   - Description: "GradeSync Pro"
   - Expires: "24 months"
   - Copy the secret value

5. **Configure Backend**
   - Update `.env`:
     ```
     OUTLOOK_CLIENT_ID=your-application-id
     OUTLOOK_CLIENT_SECRET=your-client-secret
     OUTLOOK_TENANT_ID=your-tenant-id
     ```

## Brightspace Integration

1. **Get API Credentials**
   - Contact your institution's Brightspace administrator
   - Request API access and OAuth credentials
   - Note the Brightspace URL for your institution

2. **Configure Backend**
   - Update `.env`:
     ```
     BRIGHTSPACE_URL=https://your-institution.brightspace.com
     BRIGHTSPACE_CLIENT_ID=your-client-id
     BRIGHTSPACE_CLIENT_SECRET=your-client-secret
     ```

3. **Fallback Mode**
   - If credentials not available, app uses synthetic data
   - Useful for development and testing

## Deployment

### Deploy Backend to Railway

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose GradeSync-Pro repository

3. **Configure Service**
   - Root directory: `/backend`
   - Add PostgreSQL database from Railway

4. **Add Environment Variables**
   - Add all variables from `.env`
   - Railway will provide `DATABASE_URL` dynamically

5. **Deploy**
   - Railway auto-deploys on push to main branch
   - Note your backend URL

### Deploy Frontend to Vercel

1. **Create Vercel Account**
   - Go to [vercel.com](https://vercel.com)
   - Sign up with GitHub

2. **Import Project**
   - Click "New Project"
   - Import GradeSync-Pro repository

3. **Configure Project**
   - Root directory: `/frontend`
   - Framework preset: "Create React App"
   - Build command: `npm run build`
   - Output directory: `build`

4. **Add Environment Variables**
   - Add `REACT_APP_API_URL` with your Railway backend URL

5. **Deploy**
   - Vercel auto-deploys on push to main branch

## Testing the Application

1. **Access the Application**
   - Open your Vercel URL or `http://localhost:3000`

2. **Register Account**
   - Click "Register"
   - Fill in your information
   - Submit

3. **Add a Course**
   - Click "Add Course"
   - Enter course details
   - Set target grade

4. **Define Syllabus Weights**
   - Open course
   - Click "Add Weight"
   - Add categories (Homework, Exams, etc.)
   - Ensure weights sum to 100%

5. **Add Assignments**
   - Click "Add Assignment"
   - Enter assignment details
   - Select category

6. **Enter Grades**
   - Click "Add Grade" next to assignment
   - Enter points earned
   - Save

7. **View Calculations**
   - Grade dynamically calculated
   - View breakdown by category

8. **Test Email Alerts**
   - Click "Send Grade Alert"
   - Check your email

## Troubleshooting

### Backend won't start
- Check PostgreSQL is running
- Verify DATABASE_URL is correct
- Ensure virtual environment is activated

### Frontend API errors
- Verify backend is running
- Check REACT_APP_API_URL is correct
- Check browser console for CORS errors

### Email not sending
- Verify API credentials are correct
- Check OAuth tokens are valid
- Review backend logs for errors

### Database errors
- Reset database: `db.drop_all()` then `db.create_all()`
- Check user permissions
- Verify connection string

## Support

For additional help:
- Check README.md for general info
- Review API documentation
- Open GitHub issue
- Check logs in browser console and backend terminal

## Next Steps

1. Configure email checks
2. Set up Brightspace sync schedule
3. Customize grade calculation rules
4. Add more courses and assignments
5. Monitor your grades throughout the semester!
