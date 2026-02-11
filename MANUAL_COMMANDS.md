# Eylo Project - Manual Run Commands

## 🚀 Quick Start (Local Development - No Docker)

### Step 1: Setup Virtual Environment
```powershell
cd c:\Users\shegd\OneDrive\Desktop\eylo_project2\infra
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Step 2: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 3: Run API Server (Terminal 1)
```powershell
cd c:\Users\shegd\OneDrive\Desktop\eylo_project2\infra
.\venv\Scripts\Activate.ps1
python -m app.main
```
**API will be available at:** `http://localhost:8000`

### Step 4: Run Worker (Terminal 2)
```powershell
cd c:\Users\shegd\OneDrive\Desktop\eylo_project2\infra
.\venv\Scripts\Activate.ps1
python -m app.worker
```

---

## 🐳 Alternative: Using Docker

### Start All Services
```powershell
cd c:\Users\shegd\OneDrive\Desktop\eylo_project2\infra
docker-compose up -d
```

### View Logs
```powershell
# All services
docker-compose logs -f

# Worker only
docker-compose logs -f worker

# API only
docker-compose logs -f api
```

### Stop Services
```powershell
docker-compose down
```

---

## 🧪 Testing Commands

### Health Check
```powershell
curl http://localhost:8000/health
```

### Import Test Recipe
```powershell
curl -X POST http://localhost:8000/import/recipe `
  -H "Content-Type: application/json" `
  -d '{\"url\": \"https://www.instagram.com/reel/test123/\"}'
```

### Check Database
```powershell
cd c:\Users\shegd\OneDrive\Desktop\eylo_project2\infra
.\venv\Scripts\Activate.ps1
python check_db.py
```

### Detailed Database Check
```powershell
python check_db_detailed.py
```

---

## 📦 Pre-made Batch Scripts

### Start Server
```powershell
cd c:\Users\shegd\OneDrive\Desktop\eylo_project2\infra
.\start_server.bat
```

### Run Tests
```powershell
.\run_tests.bat
```

### Test Full Flow
```powershell
.\test_full_flow.bat
```

---

## 🔧 Troubleshooting

### Reinstall Dependencies
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

### Clear Python Cache
```powershell
Get-ChildItem -Recurse -Filter "__pycache__" | Remove-Item -Recurse -Force
Get-ChildItem -Recurse -Filter "*.pyc" | Remove-Item -Force
```

### Restart Services (Docker)
```powershell
docker-compose restart api worker
```

---

## 📝 Notes

- **API Server runs on:** `http://localhost:8000`
- **API Docs available at:** `http://localhost:8000/docs`
- **Database:** SQLite (`eylo_test.db`) for local dev
- **Logs:** Check terminal output or `docker-compose logs`
