# Railway Deployment Guide

Complete guide for deploying and redeploying the Kundali API to Railway platform.

---

## Quick Summary

Your production code is ready but needs a new deployment to pick up latest fixes:
- ✅ Swisseph lazy imports (fixed)
- ✅ MongoDB schema updates (fixed)
- ✅ Response types fixed (fixed)

---

## Option 1: Web Dashboard (EASIEST - 2 minutes)

### Step 1: Access Railway Dashboard
1. Open: https://railway.app
2. Log in with GitHub account
3. Select "astrology-db" project from dropdown

### Step 2: Select Service
1. Click service name: **"astrology-db"** (web service)
2. View deployment history

### Step 3: Redeploy Service
Look for these buttons in upper right:
- **"Redeploy"** button (fastest)
- **"Rebuild"** button (rebuilds from scratch)

Click **"Redeploy"** for latest code deployment.

### Step 4: Wait for Deployment
- Status: **"Building..."** → **"Deploying..."** → **"Success"**
- Usually takes 2-3 minutes
- Watch logs for errors

### Step 5: Verify
```bash
curl https://your-railway-app.up.railway.app/health
```

Expected response:
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "database": "connected"
  }
}
```

---

## Option 2: Railway CLI (PROGRAMMATIC - 1 minute)

### Step 1: Install Railway CLI
```bash
# Via npm
npm install -g @railway/cli

# Via homebrew (Mac)
brew install railway
```

### Step 2: Login
```bash
railway login
```
Opens browser window to authenticate.

### Step 3: Link Project
```bash
cd C:\Users\ACER\Desktop\FInalProject
railway link
# Select "astrology-db" when prompted
```

### Step 4: Redeploy
```bash
railway up
```
Wait for deployment (2-3 minutes).

### Step 5: View Logs
```bash
railway logs --follow
```

---

## Option 3: Force Rebuild (Git Commit)

If Redeploy doesn't work, trigger with a commit:

```bash
cd C:\Users\ACER\Desktop\FInalProject

# Create empty commit to trigger rebuild
git commit --allow-empty -m "Force Railway redeploy - pick up latest fixes"

# Push to Railway
git push origin anup
```

Railway automatically rebuilds on push. Check dashboard for status.

---

## Environment Variables Checklist

Verify these are set in Railway Dashboard (Variables tab):

| Variable | Format | Status |
|----------|--------|--------|
| `MONGODB_URL` | `mongodb+srv://user:pass@cluster.mongodb.net/db?...` | ✅ Required |
| `SECRET_KEY` | Any string (min 32 chars, random) | ✅ Required |
| `ALGORITHM` | `HS256` | ⚠️ Optional |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `15` | ⚠️ Optional |
| `REFRESH_TOKEN_EXPIRE_DAYS` | `7` | ⚠️ Optional |

### Via CLI
```bash
# View all variables
railway variables

# Set a variable
railway variables set MONGODB_URL "mongodb+srv://..."
railway variables set SECRET_KEY "your-super-secret-key-min-32-chars"

# Redeploy
railway up
```

---

## Post-Deployment Verification

### 1. Check Health Endpoint
```bash
curl https://your-railway-app.up.railway.app/health
```
✅ Expected: `"status": "healthy"`

### 2. Test Kundali Generation
```bash
# Register user
RESPONSE=$(curl -X POST "https://your-railway-app.up.railway.app/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "name": "Test User",
    "password": "Test123!@"
  }')

TOKEN=$(echo $RESPONSE | jq -r '.data.token')

# Test kundali generation
curl -X POST "https://your-railway-app.up.railway.app/kundali/generate_kundali" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "birthDate": "1990-05-15",
    "birthTime": "14:30",
    "latitude": 28.7041,
    "longitude": 77.1025,
    "timezone": "Asia/Kolkata"
  }'
```
✅ Expected: Complete kundali data with planets, houses, dasha

### 3. Run Test Suite
```bash
python test_api_endpoints.py --url "https://your-railway-app.up.railway.app"
```
✅ Expected: All tests pass

---

## Troubleshooting

### Redeploy Button Not Available
1. Go to service settings
2. Look for "Redeploy" in top menu bar
3. Try refreshing the page

### Deployment Fails
Check logs:
```bash
railway logs --follow
```

Common errors:
- `ImportError: cannot import module` → Missing dependency
- `MongoClient connection timeout` → Database connection issue
- `SECRET_KEY not found` → Environment variable missing

### Still Getting 500 Errors After Redeploy
1. Check `SECRET_KEY` is set (can't be empty)
2. Verify `MONGODB_URL`:
   - Must have `mongodb+srv://` prefix
   - Must include username and password
   - Must have `?retryWrites=true&w=majority` at end
3. Force restart:
   ```bash
   railway restart
   ```

### Database Connection Timeout
In MongoDB Atlas console:
1. Go to Network Access
2. Ensure IP whitelist includes:
   - `0.0.0.0/0` (all IPs - simpler but less secure)
   - OR add Railway's specific IP range
3. Test connection:
   ```bash
   python -c "from server.database import health_check; print(health_check())"
   ```

---

## Monitoring After Deployment

### View Live Logs
```bash
railway logs --follow
```

### Monitor Performance
In Railway Dashboard → service → "Metrics" tab:
- CPU usage (should be low at idle)
- Memory usage (should be < 512MB)
- Response time
- Error rate (should be 0)

### Check Database Connection
```bash
curl https://your-railway-app.up.railway.app/health
```
Should include: `"database": "connected"`

---

## Checklist Before Going Live

- [ ] Code commits pushed to `origin/anup`
- [ ] All commits visible in GitHub (with fixes)
- [ ] `MONGODB_URL` set in Railway variables
- [ ] `SECRET_KEY` set in Railway variables (min 32 chars)
- [ ] Redeploy triggered and complete (no errors in logs)
- [ ] Health endpoint returns `"healthy"`
- [ ] Test suite runs successfully (all tests pass)
- [ ] No 500 errors in production logs
- [ ] Performance metrics look good (< 2000ms for kundali generation)

---

## Emergency Support

If deployment is stuck or failing:

1. **Clear Railway Cache:**
   ```bash
   railway run -- rm -rf /app/.cache
   railway up
   ```

2. **Check Environment:**
   ```bash
   railway variables
   ```
   Verify all required variables are set.

3. **Review Recent Commits:**
   ```bash
   git log --oneline -5
   ```
   Ensure commits have necessary fixes.

4. **Force Rebuild from Scratch:**
   - In Railway dashboard: service → settings → "Rebuild from scratch"
   - Or: `railway up --detach`

5. **Test Locally First:**
   ```bash
   python -m uvicorn server.main:app --port 8005
   ```
   If local works, issue is with Railway environment.

---

**Last Updated:** November 2025
