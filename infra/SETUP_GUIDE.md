# Quick Setup Guide for Real API Testing

## 1. Install Missing Dependencies

Run this in your terminal:

```powershell
pip install google-generativeai openai psycopg2-binary
```

## 2. Get Supabase Database Password

1. Go to https://supabase.com/dashboard/project/ijsbaxhpkqvxzyuwsptp
2. Click **Settings** → **Database**
3. Scroll to **Connection string**
4. Copy the password from the connection string

Or use the direct connection pooler:
- Host: `db.ijsbaxhpkqvxzyuwsptp.supabase.co`
- Port: `5432`
- Database: `postgres`
- User: `postgres.ijsbaxhpkqvxzyuwsptp`
- Password: [from dashboard]

## 3. Update .env

Replace this line in `.env`:
```
DATABASE_URL=postgresql://postgres:BFJx1F-E@db.ijsbaxhpkqvxzyuwsptp.supabase.co:5432/postgres
```

With the correct password instead of `BFJx1F-E`

## 4. Restart API Server

Stop the current server (Ctrl+C) and restart:
```powershell
python -m app.main
```

The server will create tables in your Supabase database automatically!

## 5. Test Everything

```powershell
python test_api.py
python check_db.py
```
