MANAGE := poetry run python3 manage.py


install:
	poetry install

start-production:
	poetry run gunicorn --daemon -w 5 -b 0.0.0.0:8000 game_gwent.wsgi

stop-production:
	pkill -f 'game_gwent.wsgi:application'

start:
	${MANAGE} runserver 0.0.0.0:8000

lint:
	poetry run flake8 game_gwent --exclude migrations

shell:
	${MANAGE} shell_plus --bpython

migrate:
	${MANAGE} makemigrations
	${MANAGE} migrate

build:
	make migrate
	make staticfiles

test:
	poetry run python3 manage.py test

test-coverage:
	poetry run coverage run manage.py test
	poetry run coverage report -m --include=task_manager/* --omit=task_manager/settings.py
	poetry run coverage xml --include=task_manager/* --omit=task_manager/settings.py

staticfiles:
	${MANAGE} collectstatic --no-input

load_user:
	python manage.py loaddata admin_users.json

ngrok:
	poetry run python run_ngrok.py