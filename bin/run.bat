@echo off
setlocal ENABLEDELAYEDEXPANSION

REM ============= CẤU HÌNH =============
set ENV_NAME=env
set MAIN_APP=app.py
set REQUIREMENTS=requirements.txt
set COVERAGE_DIR=htmlcov

REM ============= HÀM HỖ TRỢ =============
:usage
echo.
echo CACH SU DUNG:
echo   run.bat install       ^| Cai dat virtualenv va thu vien
echo   run.bat run           ^| Chay Flask app
echo   run.bat test          ^| Chay pytest
echo   run.bat test enable   ^| Chay pytest va do coverage
echo   run.bat clean         ^| Xoa cache va file coverage
exit /b

REM ============= XỬ LÝ CÁC THAM SỐ =============
if "%1"=="" (
    call :usage
)

if "%1"=="install" (
    echo [🔧] Tao virtualenv va cai dat thu vien...
    python -m venv %ENV_NAME%
    call %ENV_NAME%\Scripts\activate
    pip install -r %REQUIREMENTS%
    exit /b
)

if "%1"=="run" (
    echo [🚀] Chay Flask app...
    call %ENV_NAME%\Scripts\activate
    set FLASK_APP=%MAIN_APP%
    set FLASK_ENV=development
    set APP_ENV=development
    flask run
    exit /b
)

if "%1"=="test" (
    call %ENV_NAME%\Scripts\activate
    if "%2"=="enable" (
        echo [🧪] Chay test va do coverage...
        coverage run -m pytest
        coverage report
        coverage html
        echo [📊] Mo file %COVERAGE_DIR%\index.html de xem bao cao coverage
    ) else (
        echo [🧪] Chay test khong coverage...
        pytest
    )
    exit /b
)

if "%1"=="clean" (
    echo [🧹] Xoa __pycache__ va file coverage...
    for /d /r %%d in (__pycache__) do if exist "%%d" rd /s /q "%%d"
    del /q .coverage
    rd /s /q %COVERAGE_DIR%
    exit /b
)

call :usage
