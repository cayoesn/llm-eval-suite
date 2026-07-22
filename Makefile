.PHONY: run test docker-build docker-run clean

test:
	pytest --cov=app --cov-report=term-missing

docker-build:
	docker build -t llm-eval-suite .

docker-run:
	docker-compose up --build

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
