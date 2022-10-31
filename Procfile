web: python manage.py makemigrations management && python manage.py makemigrations api && python manage.py makemigrations rallytascas && python manage.py migrate && gunicorn neectrally.wsgi
worker: celery -A neectrally.celery.app worker -B --concurrency 2
