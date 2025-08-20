# Auto-pick docker compose v2 if present; else docker-compose v1
COMPOSE := $(shell if docker compose version >/dev/null 2>&1; then echo "docker compose"; else echo "docker-compose"; fi)

.PHONY: up down logs ps curl restart nuke dev

up:
	$(COMPOSE) up --build -d

down:
	$(COMPOSE) down -v

logs:
	$(COMPOSE) logs -f

ps:
	$(COMPOSE) ps

curl:
	curl http://localhost:8080/v1/health

restart:
	$(COMPOSE) restart api

nuke:
	$(COMPOSE) down -v || true; docker system prune -af

# Dev mode (hot reload via override)
dev:
	$(COMPOSE) up -d

curl-infer:
	@curl -sS -X POST http://localhost:8080/v1/infer \
	  -H "Content-Type: application/json" \
	  -d '{ "model": "demo", "version": "1.0", "inputs": {"x": [1,2,3]} }' | jq

curl-models:
	@curl -sS http://localhost:8080/v1/models | jq

curl-infer-h:
	@curl -i -sS -X POST http://localhost:8080/v1/infer \
	  -H "Content-Type: application/json" \
	  -d '{ "model": "demo", "version": "1.0", "inputs": {"x":[1,2,3]} }' | sed -n '1,25p'
curl-infer-bad:
	@echo "404 – unknown model"
	@curl -sS -X POST http://localhost:8080/v1/infer \
	  -H "Content-Type: application/json" \
	  -d '{ "model": "nope", "version": "1.0", "inputs": {"x": [1,2,3]} }' \
	  -w '\nHTTP %{http_code}\n' | jq .

curl-infer-bad-version:
	@echo "400 – version not available"
	@curl -sS -X POST http://localhost:8080/v1/infer \
	  -H "Content-Type: application/json" \
	  -d '{ "model": "demo", "version": "9.9", "inputs": {"x": [1]} }' \
	  -w '\nHTTP %{http_code}\n' | jq .

curl-infer-422:
	@echo "422 – validation error (missing inputs)"
	@curl -sS -X POST http://localhost:8080/v1/infer \
	  -H "Content-Type: application/json" \
	  -d '{ "model": "demo" }' \
	  -w '\nHTTP %{http_code}\n' | jq .
dev-setup:
	python -m pip install -r requirements.txt
	python -m pip install -r requirements-dev.txt

test:
	PYTHONPATH=. pytest -q
