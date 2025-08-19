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
