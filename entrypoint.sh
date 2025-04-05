#!/bin/bash

# Espera a que la base de datos esté lista (si usas PostgreSQL u otro servicio)
# Puedes omitir si usas SQLite
# echo "Esperando a la base de datos..."
# while ! nc -z db 5432; do sleep 0.1; done
# echo "Base de datos lista"

python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver 0.0.0.0:8000