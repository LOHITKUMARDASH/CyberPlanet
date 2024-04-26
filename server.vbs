Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "cmd /c ""C:\Users\USER\Desktop\python\venv\Scripts\activate && cd C:\Users\USER\CyberPlanet && python manage.py runserver 0.0.0.0:8000""", 0