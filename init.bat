@ECHO OFF
ECHO Generando Virtual Environment...
@python -m venv .\venv
ECHO Virtual Environment creado, procediendo a activacion...
@.\venv\Scripts\activate.bat && ECHO Virtual Environment activado, procediendo a instalacion de pips... && @pip install -r requirements.txt && ECHO Instalacion completada! && ECHO (Recuerda que puedes desactivar el ambiente con 'deactivate' en la linea de comandos)