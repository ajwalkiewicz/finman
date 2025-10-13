.PHONY: build start stop logs clean restart status publish

# Docker Compose commands
build:
	@echo "Building Docker images..."
	docker compose build

start:
	@echo "Starting Finance Manager Application with Docker Compose..."
	docker compose up -d
	@echo "Services started!"
	@echo "Backend API: http://localhost:8010"
	@echo "Frontend: http://localhost:3000" 
	@echo "Exchange Rate Proxy: http://localhost:8012"
	@echo ""
	@echo "Use 'make logs' to view logs"
	@echo "Use 'make stop' to stop services"

stop:
	@echo "Stopping services..."
	docker compose down

logs:
	@echo "Showing logs (Ctrl+C to exit)..."
	docker compose logs -f

clean:
	@echo "Stopping and removing containers, networks, and volumes..."
	docker compose down -v
	docker system prune -f

restart: stop start

status:
	@echo "Service status:"
	docker compose ps

# Legacy support
publish: scripts/publish.sh
	@echo "publishing changes..."
	./scripts/publish.sh