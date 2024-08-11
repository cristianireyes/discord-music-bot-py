#!/bin/bash

# Crear el entorno virtual si no existe
if [ ! -d "discord-bot-py-env" ]; then
    python3 -m venv discord-bot-py-env
fi

# Activar el entorno virtual
source discord-bot-py-env/Scripts/activate

# Instalar dependencias
pip install -r requirements.txt

# Iniciar la aplicación (aquí reemplaza con el comando para iniciar tu bot)
python bot.py