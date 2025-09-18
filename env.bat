@echo off
echo Creating Python 3.9 virtual environment...

REM Try different ways to find Python 3.9
py -3.9 -m venv env
if %errorlevel% neq 0 (
    python -m venv env
    if %errorlevel% neq 0 (
        echo Error: Python 3.9 not found. Please install Python 3.9 first.
        echo Download from: https://www.python.org/downloads/release/python-3918/
        pause
        exit /b 1
    )
)

echo Activating environment...
call env\Scripts\activate

echo Upgrading pip...
python -m pip install --upgrade pip

if exist requirements.txt (
    echo Installing from requirements.txt...
    pip install -r requirements.txt
) else (
    echo requirements.txt not found, creating default one...
    echo # Python 3.9 Compatible Versions > requirements.txt
    echo pywebview==4.2.2 >> requirements.txt
    echo pyinstaller==5.13.0 >> requirements.txt
    echo pillow==9.5.0 >> requirements.txt
    echo requests==2.31.0 >> requirements.txt
    echo urllib3==1.26.16 >> requirements.txt
    echo pywin32==306 >> requirements.txt
    echo pygame==2.5.0 >> requirements.txt
    echo numpy==1.24.3 >> requirements.txt
    echo pygame_gui==0.6.9 >> requirements.txt
    echo python-dateutil==2.8.2 >> requirements.txt
    pip install -r requirements.txt
)

echo.
echo Environment setup complete!
echo To activate the environment in the future, run: env\Scripts\activate
call env\Scripts\deactivate
pause