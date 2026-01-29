@echo off
echo ========================================
echo Eylo Backend - Full Flow Test
echo ========================================
echo.
echo This will test the complete recipe import flow.
echo Make sure the API server and worker are running!
echo.
echo Step 1: Creating a new recipe import job...
python test_real_reel.py
echo.
echo Step 2: Checking database for results...
timeout /t 3 >nul
python check_db.py
echo.
echo ========================================
echo Test Complete!
echo ========================================
pause
