call .\env\Scripts\activate.bat
call pip install auto-py-to-exe
call pyinstaller -y -w  "GUI.py"
start "" ".\dist\GUI\GUI.exe"