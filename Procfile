web: gunicorn backend.wsgi
release: python manage.py migrate && python manage.py createsuperuser --noinput
