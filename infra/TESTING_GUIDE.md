# Complete Backend Testing Guide

## Quick Test - See It Working Now!

### Terminal Setup (3 terminals needed)

#### Terminal 1: API Server
```powershell
cd C:\Users\shegd\OneDrive\Desktop\eylo_project2\infra
python -m app.main
```
**Status:** Keep running ✓

---

#### Terminal 2: Worker (START THIS FIRST!)
```powershell
cd C:\Users\shegd\OneDrive\Desktop\eylo_project2\infra
python -m app.worker
```
**Status:** Keep running ✓

---

#### Terminal 3: Test Commands
```powershell
cd C:\Users\shegd\OneDrive\Desktop\eylo_project2\infra

# Create a job (worker will pick it up immediately!)
python test_real_reel.py

# Wait 2-3 seconds, then check database
python check_db.py
```

---

## What You'll See

### In Terminal 2 (Worker Logs):
```
Processing job [id]...
Scraping Instagram...
❌ Error: Instagram scraping failed (test Apify token)
Job marked as failed in database
```

**This is EXPECTED!** The scraping fails because you're using a test Apify token, but you'll see:
- ✅ Worker picks up the job
- ✅ Attempts to process it
- ✅ Saves job record to database

---

## Next Steps After Testing

### Option A: Get Real Apify Token
Get actual Instagram scraping working:
1. Sign up at https://console.apify.com/
2. Get your API token
3. Update `.env`: `APIFY_API_TOKEN=your_real_token`
4. Restart worker and test again!

### Option B: Mobile App Integration
Connect your Eylo mobile app:
1. Find your computer's local IP: `ipconfig` (look for IPv4)
2. Update app API URL to `http://YOUR_IP:8000`
3. Test share sheet → backend flow
4. See recipe imports in the app!

### Option C: Deploy to Production
Make it live:
1. Choose a platform (Railway, Render, AWS)
2. Set up environment variables
3. Deploy the `infra` folder
4. Update mobile app to production URL

---

## Troubleshooting

**Worker doesn't pick up jobs:**
- Make sure worker is running BEFORE creating jobs
- In-memory queue doesn't persist - start worker first!

**Database shows no jobs:**
- Check that worker processed the job (look at Terminal 2 logs)
- Run `python check_db.py` after seeing worker logs

**Import fails with errors:**
- Instagram scraping: Need real Apify token
- S3 upload: Need real AWS credentials
- Notifications: Need Firebase configuration
