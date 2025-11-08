# Production Deployment Guide

## Overview

This guide covers deploying the Kundali Astrology API to production using Supabase PostgreSQL and any Python-capable hosting service.

---

## Pre-Deployment Checklist

- [ ] Supabase project created with PostgreSQL database
- [ ] Database credentials obtained from Supabase dashboard
- [ ] Production environment configured with `.env` file
- [ ] All Python dependencies installed
- [ ] Code tested locally
- [ ] API documentation reviewed

---

## Environment Configuration

### 1. Create Production `.env` File

Replace with your actual Supabase credentials:

```bash
# Database Configuration
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@YOUR_SUPABASE_HOST:5432/postgres

# JWT Configuration
SECRET_KEY=YOUR_SECURE_RANDOM_KEY  # Generate: python -c "import secrets; print(secrets.token_urlsafe(32))"
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# Environment
ENVIRONMENT=production

# API Configuration
API_PORT=8001
API_HOST=0.0.0.0
API_WORKERS=4

# Logging
LOG_LEVEL=INFO
```

### 2. Obtain Supabase Credentials

1. Go to [Supabase Dashboard](https://app.supabase.com)
2. Select your project
3. Click "Settings" → "Database"
4. Copy the "Connection String (URI)" under "Connection pooling"
5. Replace `[YOUR-PASSWORD]` with your database password

---

## Deployment Methods

### Method 1: Heroku (Free Tier Available)

#### Step 1: Install Heroku CLI
```bash
# Windows
choco install heroku-cli

# macOS
brew tap heroku/brew && brew install heroku
```

#### Step 2: Create Procfile
```bash
# In project root
echo "web: python deploy_production.py" > Procfile
```

#### Step 3: Create app.json
```json
{
  "name": "kundali-astrology-api",
  "description": "Vedic Astrology API with ML predictions",
  "buildpacks": [
    {
      "url": "heroku/python"
    }
  ],
  "env": {
    "DATABASE_URL": {
      "description": "Supabase PostgreSQL connection string"
    },
    "SECRET_KEY": {
      "description": "JWT secret key"
    },
    "ALGORITHM": {
      "value": "HS256"
    },
    "ACCESS_TOKEN_EXPIRE_MINUTES": {
      "value": "15"
    },
    "REFRESH_TOKEN_EXPIRE_DAYS": {
      "value": "7"
    }
  }
}
```

#### Step 4: Deploy
```bash
heroku login
heroku create your-app-name
heroku config:set DATABASE_URL="your_connection_string"
heroku config:set SECRET_KEY="your_secret_key"
git push heroku main
heroku logs --tail
```

---

### Method 2: Railway (Recommended)

#### Step 1: Sign Up
Visit [Railway.app](https://railway.app) and sign up with GitHub

#### Step 2: Create New Project
1. Click "New Project"
2. Select "Deploy from GitHub"
3. Connect your repository

#### Step 3: Add PostgreSQL
1. Click "Add Service"
2. Select "PostgreSQL"
3. Railway will auto-configure DATABASE_URL

#### Step 4: Set Environment Variables
1. In Railway dashboard, go to your project
2. Select the Python service
3. Add variables under "Variables":
   - `SECRET_KEY`
   - `ALGORITHM=HS256`
   - `ACCESS_TOKEN_EXPIRE_MINUTES=15`
   - `REFRESH_TOKEN_EXPIRE_DAYS=7`

#### Step 5: Deploy
Push to main branch - Railway auto-deploys

---

### Method 3: Google Cloud Run (Scalable)

#### Step 1: Install Google Cloud SDK
```bash
# Download from https://cloud.google.com/sdk/docs/install
```

#### Step 2: Create Dockerfile
```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8001
EXPOSE 8001

CMD ["python", "deploy_production.py"]
```

#### Step 3: Create Cloud Run Service
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Build and deploy
gcloud run deploy kundali-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars DATABASE_URL="your_url",SECRET_KEY="your_key"
```

---

### Method 4: DigitalOcean App Platform

#### Step 1: Prepare app.yaml
```yaml
name: kundali-api
services:
- name: api
  source:
    type: github
    repo: YOUR_GITHUB_REPO
    branch: main
  build_command: pip install -r requirements.txt
  run_command: python deploy_production.py
  http_port: 8001
  envs:
  - key: DATABASE_URL
    scope: RUN_AND_BUILD_TIME
    value: ${DATABASE_URL}
  - key: SECRET_KEY
    scope: RUN_AND_BUILD_TIME
    value: ${SECRET_KEY}
```

#### Step 2: Deploy
1. Go to [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)
2. Click "Create App"
3. Select GitHub and connect repository
4. Upload app.yaml
5. Set environment variables
6. Click "Deploy"

---

## Post-Deployment Steps

### 1. Initialize Database Tables
```bash
# Run once on first deployment
python -c "from server.database import init_db; init_db()"
```

Or the deployment script will do this automatically.

### 2. Verify Health Check
```bash
curl https://your-app-url/health
```

Expected response:
```json
{
  "success": true,
  "status": "SUCCESS",
  "data": {
    "status": "healthy",
    "ephemeris": "initialized",
    "database": "connected"
  }
}
```

### 3. Test Authentication
```bash
# Register a user
curl -X POST https://your-app-url/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "test_password_123",
    "full_name": "Test User"
  }'
```

### 4. Monitor Logs
- **Heroku**: `heroku logs --tail`
- **Railway**: Dashboard → Deployments → Logs
- **Cloud Run**: `gcloud run logs read kundali-api`
- **DigitalOcean**: App Dashboard → Runtime Logs

---

## Database Backup Strategy

### Enable Automated Backups in Supabase
1. Go to Supabase Dashboard
2. Select your project
3. Click "Backups" in sidebar
4. Enable automated backups
5. Configure backup frequency (daily recommended)

### Manual Backup
```bash
# Using pg_dump
pg_dump "your_connection_string" > backup.sql

# Upload to Cloud Storage
# Backup to GitHub, S3, or GCS
```

---

## Monitoring and Alerts

### Set Up Error Tracking (Optional)
```bash
# Install Sentry for error monitoring
pip install sentry-sdk

# In server/main.py, add:
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="YOUR_SENTRY_DSN",
    integrations=[FastApiIntegration()],
    traces_sample_rate=0.1
)
```

### Monitor Key Metrics
- API response times
- Database connection pool usage
- JWT token generation rate
- User registration/login attempts
- Error rates

---

## Security Considerations

### 1. HTTPS/TLS
- All deployment platforms provide free HTTPS
- Ensure HTTPS is enforced

### 2. Database Security
- Use strong passwords (Supabase generates these)
- Enable Row Level Security (RLS) in Supabase
- Restrict database access to API only
- Regular security updates

### 3. API Security
- Keep SECRET_KEY secret (never commit to Git)
- Rotate SECRET_KEY periodically
- Implement rate limiting
- Use CORS carefully

### 4. Environment Variables
- Use platform secrets for sensitive data
- Never hardcode credentials
- Rotate keys regularly

### .gitignore
Ensure these files are not committed:
```
.env
.env.production
*.pem
*.key
```

---

## Troubleshooting

### Database Connection Error
```
Error: could not translate host name "db.xxxx.supabase.co"
```

**Solution:**
- Check internet connectivity
- Verify DATABASE_URL is correct
- Ensure firewall allows outbound connections
- Check Supabase dashboard for service status

### Token Signature Verification Failed
```
Error: token signature verification failed
```

**Solution:**
- Ensure SECRET_KEY is consistent across deployments
- Don't rotate SECRET_KEY while tokens are valid
- Check timezone configuration (should be UTC)

### Insufficient Disk Space
**Solution:**
- Check log files and archive old logs
- Clean up temporary files
- Increase storage in hosting plan

### High Database Connection Pool Usage
**Solution:**
- Enable connection pooling in Supabase
- Reduce pool size if too high
- Implement connection pooling timeout

---

## Scaling in Production

### Horizontal Scaling
- Most platforms support auto-scaling
- Set CPU threshold at 70-80%
- Monitor database connection limits

### Vertical Scaling
- Increase instance size as needed
- Monitor RAM and CPU usage
- Plan capacity ahead of growth

### Database Optimization
1. Add indexes for frequently queried fields
2. Archive old prediction data
3. Use read replicas for high-traffic queries
4. Consider caching with Redis (future)

---

## Performance Optimization

### API Server
```python
# Use multiple workers
API_WORKERS=4  # 2-4x number of CPU cores

# Enable compression
# Configure in middleware

# Cache responses
# Implement HTTP caching headers
```

### Database
- Enable query logging to identify slow queries
- Use EXPLAIN ANALYZE to optimize queries
- Add appropriate indexes
- Archive old data periodically

---

## Maintenance Schedule

### Daily
- Check error logs
- Monitor API health
- Verify backup completion

### Weekly
- Review performance metrics
- Check database size
- Analyze user patterns

### Monthly
- Review security logs
- Update dependencies
- Test disaster recovery
- Optimize database queries

### Quarterly
- Security audit
- Capacity planning
- Performance review
- Update documentation

---

## Rollback Plan

If deployment fails:

```bash
# Revert to previous version
git revert HEAD
git push

# OR

# Redeploy previous commit
git push origin previous_commit:main

# Check logs for issues
# Fix bugs locally
# Test thoroughly
# Redeploy when ready
```

---

## Support and Documentation

- **API Docs**: Available at `/docs` (Swagger UI)
- **Error Reference**: See [API_DOCUMENTATION_DATABASE.md](API_DOCUMENTATION_DATABASE.md)
- **Implementation Details**: See [DATABASE_IMPLEMENTATION_SUMMARY.md](DATABASE_IMPLEMENTATION_SUMMARY.md)

---

## Deployment Checklist - Pre-Launch

- [ ] .env file configured with production credentials
- [ ] All tests passing
- [ ] No hardcoded secrets in codebase
- [ ] API documentation reviewed
- [ ] Database backup strategy implemented
- [ ] Monitoring/alerting configured
- [ ] Error handling tested
- [ ] SSL/TLS enabled
- [ ] CORS configured correctly
- [ ] Rate limiting considered
- [ ] Logging configured
- [ ] Deployment script tested

---

## Success Indicators

After successful deployment, verify:
- [ ] API is accessible via HTTPS
- [ ] Health check endpoint returns "healthy"
- [ ] Registration endpoint creates users
- [ ] Login endpoint returns valid tokens
- [ ] Kundali endpoints work with authentication
- [ ] Prediction endpoints save data
- [ ] Logs show no errors
- [ ] Response times < 500ms
- [ ] Database connections stable

---

Congratulations! Your API is now in production!
