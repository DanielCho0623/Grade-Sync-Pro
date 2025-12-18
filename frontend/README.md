# GradeSync Pro Frontend

React-based frontend application for GradeSync Pro.

## Features

- Modern React 18 application
- JWT authentication with context
- Responsive design
- Real-time grade monitoring
- Course and assignment management
- Email notification controls

## Pages

### Login/Register
- User authentication
- JWT token management
- Protected routes

### Dashboard
- Course overview cards
- Grade summaries
- Quick actions
- Add new courses

### Course Detail
- Grade breakdown
- Syllabus weight management
- Assignment tracking
- Grade entry
- Brightspace sync
- Email alerts

## Components

### Navbar
- Application header
- User menu
- Logout functionality

### Modals
- Add Course
- Add Weight
- Add Assignment
- Add/Update Grade

## State Management

Uses React Context for:
- Authentication state
- User data
- JWT token

## API Integration

All API calls through `services/api.js`:
- Axios instance with interceptors
- Automatic JWT token injection
- Error handling
- Auto-redirect on 401

## Styling

- Custom CSS in `App.css`
- Responsive grid layouts
- Card-based UI
- Color-coded grade badges

## Running

Development:
```bash
npm start
```

Production build:
```bash
npm run build
```

## Deployment

Configured for Vercel deployment with:
- `vercel.json` - Routing configuration
- Environment variables for API URL
- SPA fallback to index.html
