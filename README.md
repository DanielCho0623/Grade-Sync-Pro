<<<<<<< HEAD
<<<<<<< HEAD
# GradeSync Pro

Track your grades and get email alerts when they drop.

## Features

- Add courses and assignments
- Calculate final grades with syllabus weights
- Get email alerts when grades are low
- Sync with Brightspace

## Tech

**Frontend:** React + Vercel
**Backend:** Flask + PostgreSQL + Railway
**APIs:** Brightspace, Gmail

**Live:** [grade-sync-pro.vercel.app](https://grade-sync-pro.vercel.app)

## Setup

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py

Frontend:

cd frontend
npm install
npm start

How it works
Add your courses
Set grade weights (homework 30%, exams 40%, etc)
Add assignments and grades
App calculates your final grade
Get email if grade drops below target

=======
# GradeSync-Pro
>>>>>>> 467074f (initial commit)
=======
# GradeSync Pro

A full-stack web application for grade tracking and monitoring with Brightspace integration, syllabus-defined weights, and real-time email notifications.

## Features

- **Full-Stack Architecture**: React.js frontend with Python Flask backend and PostgreSQL database
- **JWT Authentication**: Secure user authentication and authorization
- **Brightspace Integration**: Sync courses, assignments, and grades from Brightspace (with synthetic data fallback)
- **grade Calculation**: Calculate final grades based on syllabus-defined category weights
- **Real-Time Monitoring**: Track grade progress and project final grades
- **Email Notifications**: alerts via Gmail and Outlook APIs when grades fall below targets
- **Course Management**: Add courses, define syllabus weights, manage assignments
- **Grade Analytics**: View detailed grade breakdowns by category
- **Responsive UI**: Modern, intuitive interface built with React

## Tech Stack

### Frontend
- React.js 18.2
- React Router for navigation
- Axios for API calls
- Recharts for data visualization
- Deployed on Vercel

### Backend
- Python 3.11
- Flask 3.0 web framework
- PostgreSQL database
- SQLAlchemy ORM
- JWT authentication
- Deployed on Railway

### APIs & Integrations
- Brightspace API
- Gmail API (OAuth 2.0)
- Microsoft Graph API (Outlook)

### DevOps
- GitHub Actions for CI/CD
- testing
- Docker support

## Project Structure

```
GradeSync-Pro/
├── backend/
│   ├── app/
│   │   ├── models/          # Database models
│   │   ├── routes/          # API endpoints
│   │   ├── services/        # External service integrations
│   │   └── utils/           # Utility functions
│   ├── tests/               # Backend tests
│   ├── config.py            # Configuration
│   ├── requirements.txt     # Python dependencies
│   └── app.py              # Application entry point
├── frontend/
│   ├── public/             # Static files
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── contexts/       # React contexts
│   │   ├── pages/          # Page components
│   │   └── services/       # API services
│   └── package.json        # Node dependencies
└── .github/
    └── workflows/          # CI/CD pipelines
```

## Setup Instructions

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Gmail/Outlook API credentials (optional)
- Brightspace API credentials (optional)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Initialize the database:
```bash
python
>>> from app import create_app, db
>>> app = create_app()
>>> with app.app_context():
...     db.create_all()
```

6. Run the development server:
```bash
python app.py
```

The backend API will be available at `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API URL
```

4. Run the development server:
```bash
npm start
```

The frontend will be available at `http://localhost:3000`

## API Documentation

### Authentication Endpoints

#### Register
```
POST /api/auth/register
Body: {
  "email": "user@example.com",
  "password": "password",
  "first_name": "John",
  "last_name": "Doe"
}
```

#### Login
```
POST /api/auth/login
Body: {
  "email": "user@example.com",
  "password": "password"
}
Response: {
  "access_token": "jwt_token",
  "user": {...}
}
```

### Course Endpoints

#### Get All Courses
```
GET /api/courses/
Headers: { "Authorization": "Bearer <token>" }
```

#### Create Course
```
POST /api/courses/
Headers: { "Authorization": "Bearer <token>" }
Body: {
  "course_code": "CS 3520",
  "course_name": "Programming in C++",
  "semester": "Spring",
  "year": 2025,
  "target_grade": 85.0
}
```

#### Calculate Grade
```
GET /api/courses/<id>/calculate
Headers: { "Authorization": "Bearer <token>" }
Response: {
  "final_grade": 87.5,
  "projected_final_grade": 88.2,
  "letter_grade": "B+",
  "breakdown": [...]
}
```

### Grade Endpoints

#### Add/Update Grade
```
POST /api/grades/assignment/<assignment_id>
Headers: { "Authorization": "Bearer <token>" }
Body: {
  "points_earned": 85,
  "feedback": "Great work!"
}
```

### Notification Endpoints

#### Send Grade Alert
```
POST /api/notifications/send-grade-alert/<course_id>
Headers: { "Authorization": "Bearer <token>" }
Body: {
  "use_gmail": true,
  "use_outlook": true
}
```

## Deployment

### Backend (Railway)

1. Connect your GitHub repository to Railway
2. Select the `backend` directory as the root
3. Add environment variables in Railway dashboard
4. Railway will dynamically deploy using the `Procfile`

### Frontend (Vercel)

1. Connect your GitHub repository to Vercel
2. Select the `frontend` directory as the root
3. Add environment variables in Vercel dashboard
4. Set build command: `npm run build`
5. Set output directory: `build`

## Email Notification Setup

### Gmail API

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project
3. Enable Gmail API
4. Create OAuth 2.0 credentials
5. Download credentials and save as `credentials/gmail_credentials.json`

### Outlook API

1. Go to [Azure Portal](https://portal.azure.com)
2. Register a new application
3. Add Mail.Send permission
4. Create a client secret
5. Add credentials to `.env` file

## Usage

1. **Register/Login**: Create an account or log in
2. **Add Courses**: Create courses for the current semester
3. **Define Weights**: Set up syllabus weights for each category (Homework, Exams, etc.)
4. **Sync from Brightspace**: Import assignments and grades dynamically
5. **Manual Entry**: Add assignments and grades manually if needed
6. **Monitor Grades**: View real-time grade calculations and projections
7. **Email Alerts**: Receive notifications when grades fall below targets

## Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Contact

For questions or support, please open an issue on GitHub.

## Acknowledgments

- Built with Flask, React, and PostgreSQL
- Integrates with Brightspace, Gmail, and Outlook APIs
- Deployed on Railway and Vercel
>>>>>>> c16e90d (add documentation)
