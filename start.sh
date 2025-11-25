#!/bin/bash
set -e

echo "🔍 DIAGNÓSTICO DE DIRETÓRIO:"
echo "📂 Pasta atual (PWD):"
pwd

echo "📄 Arquivos nesta pasta:"
ls -la

echo "🚀 Iniciando Deploy..."

echo "🔄 Rodando Migrations..."
python manage.py migrate --noinput

echo "🔥 Iniciando Servidor..."
# Adicionei o ./ para forçar o diretório atual, mas o ls acima vai nos dizer a verdade
gunicorn core.wsgi:application --config ./gunicorn_config.py