dev:
	poetry run flask --app page_analyzer:app run

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app


black:
	poetry run black page_analyzer

flake8:
	poetry run flake8 page_analyzer/