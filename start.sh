#!/bin/bash
set -e

echo "🚀 Iniciando Deploy..."

echo "🔄 Rodando Migrations..."
python manage.py migrate --noinput

echo "🔥 Iniciando Servidor (Config Hardcoded)..."
# Aqui colocamos as configs direto no comando, sem precisar do arquivo .py
gunicorn core.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --threads 4 \
    --timeout 60 \
    --keep-alive 5 \
    --access-logfile - \
    --error-logfile - \
    --log-level info