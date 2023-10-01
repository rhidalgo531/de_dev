.PHONY: up up-verbose down

# Default target when running 'make' without arguments
default: up

# Start the Docker Compose services in the background (daemon mode)
up:
	docker-compose up -d

# Start the Docker Compose services in the foreground with verbose output
up-verbose:
	docker-compose up --timestamps 

# Stop and remove the Docker Compose services
down:
	docker-compose down