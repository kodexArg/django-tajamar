#!/bin/bash
set -e

# Crear entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
echo "Dependencies installed."

# Crear directorios necesarios
mkdir -p nginx/certs nginx/daphne staticfiles static media
echo "Necessary directories created."

# Crear certificados SSL
if [ ! -f nginx/certs/nginx-selfsigned.key ] || [ ! -f nginx/certs/nginx-selfsigned.crt ]; then
  openssl genpkey -algorithm RSA -out nginx/certs/nginx-selfsigned.key
  openssl req -new -x509 -key nginx/certs/nginx-selfsigned.key -out nginx/certs/nginx-selfsigned.crt -days 365 -subj "/CN=localhost"
  echo "SSL certificates created."
else
  echo "SSL certificates already exist."
fi

# Comunicar la finalización
echo "Initialization complete. You can now start the project with 'docker compose up --build'."
