release: python manage.py migrate --noinput
web: gunicorn src.wsgi:application --log-file - --log-level debug
worker: celery worker -A src.celery --loglevel=info --concurrency=4
