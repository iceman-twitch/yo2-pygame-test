@echo off
echo Activating Python environment...
call env\Scripts\activate

echo Running PyInstaller on form.py...
pyinstaller --onefile --windowed --name "yo2_launcher" --icon="yo2.ico" launcher.py

echo.
echo Build complete! Check the 'dist' folder for your executable.
call env\Scripts\deactivate
pause