SHELL = cmd

PYTHON = python

.PHONY = help setup deactivate run 

.DEFAULT_GOAL = help

help:
		@echo ---------------HELP-----------------
		@echo Para alistar el projecto escribir setup
		@echo Para ejecutar el projecto escribir run
		@echo ------------------------------------


setup:
		@echo ================================ SETUP ===================================
		@echo Generando Virtual Environment...
		${PYTHON} -m venv .\venv
		@echo Virtual Environment creado, procediendo a activacion...
		cmd /C .\venv\Scripts\activate.bat
		@echo Virtual Environment activado, procediendo a instalacion de paquetes...
		pip install -r requirements.txt
		@echo Instalacion completada!
		@echo (Recuerda que puedes desactivar el ambiente con 'deactivate' en la linea de comandos)

run:
		${PYTHON} main.py
