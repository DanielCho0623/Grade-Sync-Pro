# Deployment Guide

This guide walks you through deploying GradeSync Pro to Railway (backend) and Vercel (frontend).

## Prerequisites

- GitHub account
- Railway account (https://railway.app)
- Vercel account (https://vercel.com)
- Your code pushed to GitHub

## Part 1: Deploy Backend to Railway

### Step 1: Create Railway Project

1. Go to https://railway.app and sign in
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your `GradeSync-Pro` repository
5. Railway will automatically detect it's a Python app

### Step 2: Configure Railway

1. **Set Root Directory:**
   - Click on your service
   - Go to "Settings" tab
   - Under "Build & Deploy", set Root Directory to: `backend`

2. **Add PostgreSQL Database:**
   - Click "New" → "Database" → "Add PostgreSQL"
   - Railway will automatically create a PostgreSQL database
   - The `DATABASE_URL` environment variable will be auto-configured

### Step 3: Set Environment Variables

In Railway dashboard, go to "Variables" tab and add:

```
FLASK_ENV=production
SECRET_KEY=<generate-a-random-secret-key>
JWT_SECRET_KEY=<generate-a-random-jwt-secret>
ALERT_EMAIL=your-email@example.com
GRADE_THRESHOLD=85.0
USE_SYNTHETIC_DATA=false
```

**Optional (for real email sending):**
```
GMAIL_CLIENT_ID=your-gmail-client-id
GMAIL_CLIENT_SECRET=your-gmail-client-secret
GMAIL_REFRESH_TOKEN=your-gmail-refresh-token
```

**To generate secret keys:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Step 4: Deploy

1. Click "Deploy"
2. Wait for build to complete (~2-3 minutes)
3. Once deployed, click "Settings" and copy your Railway app URL
   - It will look like: `https://your-app.up.railway.app`
4. **Important:** Add this environment variable with your soon-to-be Vercel URL:
   ```
   FRONTEND_URL=https://your-app.vercel.app
   ```
   (You'll update this in Step 8 after deploying frontend)

## Part 2: Deploy Frontend to Vercel

### Step 5: Create Vercel Project

1. Go to https://vercel.com and sign in
2. Click "Add New Project"
3. Import your `GradeSync-Pro` repository
4. Vercel will detect it's a React app

### Step 6: Configure Vercel

1. **Set Root Directory:**
   - Under "Build and Output Settings"
   - Set Root Directory to: `frontend`

2. **Build Settings:**
   - Build Command: `npm run build` (auto-detected)
   - Output Directory: `build` (auto-detected)
   - Install Command: `npm install` (auto-detected)

### Step 7: Set Environment Variables

In Vercel project settings, add environment variable:

```
REACT_APP_API_URL=https://your-railway-app.up.railway.app/api
```

Replace `your-railway-app.up.railway.app` with your actual Railway URL from Step 4.

### Step 8: Deploy

1. Click "Deploy"
2. Wait for build to complete (~2-3 minutes)
3. Once deployed, copy your Vercel app URL
   - It will look like: `https://your-app.vercel.app`

### Step 9: Update Railway with Frontend URL

1. Go back to Railway
2. In your backend service, add/update the environment variable:
   ```
   FRONTEND_URL=https://your-actual-app.vercel.app
   ```
3. Railway will automatically redeploy with the new CORS settings

## Part 3: Verify Deployment

### Test Your Deployed App

1. **Open your Vercel URL** in a browser
2. **Register a new account**
3. **Check if courses are auto-imported**
4. **Click "Check All Grades"** to test email functionality
5. **Check your email** (if Gmail OAuth is configured)

### Troubleshooting

**Backend not connecting to frontend:**
- Check `FRONTEND_URL` is set correctly in Railway
- Check `REACT_APP_API_URL` is set correctly in Vercel
- Both should be HTTPS URLs

**Database errors:**
- Railway PostgreSQL should be automatically connected
- Check `DATABASE_URL` exists in Railway variables
- Check Railway logs for database connection errors

**Email not sending:**
- Verify `GMAIL_CLIENT_ID`, `GMAIL_CLIENT_SECRET`, and `GMAIL_REFRESH_TOKEN` are set
- Check `USE_SYNTHETIC_DATA=false` in Railway
- Check Gmail API is enabled in Google Cloud Console

**CORS errors:**
- Verify `FRONTEND_URL` matches your exact Vercel URL
- Check Railway logs for CORS errors
- Make sure both services are deployed and running

## Updating Your Deployment

Whenever you push new code to GitHub:

1. **Automatic Deployment:**
   - Both Railway and Vercel will automatically rebuild and redeploy
   - Check the deployment status in their dashboards

2. **Manual Deployment:**
   - Railway: Click "Deployments" → "Deploy"
   - Vercel: Click "Deployments" → "Redeploy"

## Viewing Logs

**Railway Logs:**
- Go to your Railway project
- Click "Deployments"
- Click on latest deployment
- Click "View Logs"

**Vercel Logs:**
- Go to your Vercel project
- Click "Deployments"
- Click on latest deployment
- View build and runtime logs

## Environment Variables Summary

### Backend (Railway)

Required:
- `DATABASE_URL` (auto-set by Railway PostgreSQL)
- `FLASK_ENV=production`
- `SECRET_KEY`
- `JWT_SECRET_KEY`
- `FRONTEND_URL` (your Vercel URL)
- `USE_SYNTHETIC_DATA=false`

Optional:
- `GMAIL_CLIENT_ID`, `GMAIL_CLIENT_SECRET`, `GMAIL_REFRESH_TOKEN`
- `OUTLOOK_CLIENT_ID`, `OUTLOOK_CLIENT_SECRET`
- `BRIGHTSPACE_URL`, `BRIGHTSPACE_CLIENT_ID`, `BRIGHTSPACE_CLIENT_SECRET`

### Frontend (Vercel)

Required:
- `REACT_APP_API_URL` (your Railway URL + /api)

## Post-Deployment Checklist

- [ ] Backend is accessible at Railway URL
- [ ] Frontend is accessible at Vercel URL
- [ ] Can register a new account
- [ ] Can login
- [ ] Courses are auto-imported
- [ ] Grades are calculated correctly
- [ ] Email alerts work (if configured)
- [ ] No CORS errors in browser console
- [ ] No errors in Railway logs
- [ ] No errors in Vercel logs

## Next Steps

- Add your deployment URLs to your resume
- Share the live demo link
- Continue adding features and redeploying
- Monitor Railway and Vercel usage/costs

## Support

If you encounter issues:
- Check Railway logs for backend errors
- Check Vercel logs for frontend errors
- Check browser console for client-side errors
- Verify all environment variables are set correctly
