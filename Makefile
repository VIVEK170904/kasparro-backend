up:
	docker compose up --build

down:
	docker compose down

test:
	docker compose run app pytest
rebuild:
	docker compose up --build --force-recreate
