#!/bin/bash

# Para o script se der erro em qualquer comando
set -e

echo "🚀 Iniciando Deploy..."

# 1. Aplica as migrações no banco de dados
echo "🔄 Rodando Migrations..."
python manage.py migrate --noinput

# 2. Inicia o Gunicorn com a config otimizada
echo "🔥 Iniciando Servidor..."
gunicorn core.wsgi:application --config gunicorn_config.py