@echo off
echo ========================================
echo Eylo Backend Testing Script
echo ========================================
echo.

echo Step 1: Checking database...
python check_db.py
echo.

echo Step 2: Testing API endpoints...
python test_api.py
echo.

echo ========================================
echo Tests Complete!
echo ========================================
pause
