web: gunicorn backend.wsgi
release: python manage.py makemigrations tasks && python manage.py migrate tasks
worker: celery -A backend worker --loglevel=info
