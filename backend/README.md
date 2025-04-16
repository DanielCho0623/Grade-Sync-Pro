# GradeSync Pro Backend

Flask-based RESTful API server for GradeSync Pro.

## Features

- RESTful API with Flask
- PostgreSQL database with SQLAlchemy ORM
- JWT-based authentication
- Brightspace API integration
- Email notifications (Gmail & Outlook)
<<<<<<< HEAD
- grade calculations
=======
- Automated grade calculations
>>>>>>> c16e90d (add documentation)
- Comprehensive test coverage

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user
- `PUT /api/auth/me` - Update user profile

### Courses
- `GET /api/courses/` - List all courses
- `POST /api/courses/` - Create course
- `GET /api/courses/<id>` - Get course details
- `PUT /api/courses/<id>` - Update course
- `DELETE /api/courses/<id>` - Delete course
- `POST /api/courses/<id>/sync` - Sync from Brightspace
- `GET /api/courses/<id>/calculate` - Calculate current grade
- `POST /api/courses/<id>/weights` - Add syllabus weight
- `POST /api/courses/<id>/assignments` - Add assignment

### Grades
- `POST /api/grades/assignment/<id>` - Add/update grade
- `GET /api/grades/assignment/<id>` - Get grade
- `DELETE /api/grades/assignment/<id>` - Delete grade
- `GET /api/grades/course/<id>` - Get all course grades

### Notifications
- `GET /api/notifications/` - List notifications
- `PUT /api/notifications/<id>/read` - Mark as read
- `POST /api/notifications/send-grade-alert/<course_id>` - Send alert
- `POST /api/notifications/auto-check` - Check all courses

## Database Models

### User
- email, password_hash
- first_name, last_name
- brightspace_user_id

### Course
- course_code, course_name
- semester, year
- target_grade

### Assignment
- name, category
- max_points, due_date

### Grade
- points_earned, percentage
- letter_grade, feedback

### SyllabusWeight
- category, weight
- description

### Notification
- notification_type, subject
- message, sent_via

## Configuration

Environment variables (see `.env.example`):
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - Flask secret key
- `JWT_SECRET_KEY` - JWT signing key
- `BRIGHTSPACE_*` - Brightspace API credentials
- `GMAIL_*` - Gmail API credentials
- `OUTLOOK_*` - Outlook API credentials

## Running Tests

```bash
pytest tests/ -v
```

## Deployment

Configured for Railway deployment with:
- `Procfile` - Gunicorn configuration
- `railway.json` - Railway settings
- `nixpacks.toml` - Build configuration
