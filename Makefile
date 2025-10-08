.PHONY: up down test fmt lint ingest

up:
	docker-compose up --build

down:
	docker-compose down -v

test:
	pytest -q

fmt:
	black .

lint:
	flake8

ingest:
	python scripts/generate_sample_logs.py | bash scripts/ingest_sample.sh


