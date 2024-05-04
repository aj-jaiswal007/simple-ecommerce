# restart command to run docker-compose down build and up
restart:
	docker-compose down
	docker-compose build
	docker-compose up

# Generates the migration
generate:
	export DATABASE_HOST=localhost && alembic revision --autogenerate -m "migration"

# Migrates the PG DB
migrate:
	export DATABASE_HOST=localhost && alembic upgrade head


# PHONY commands
.PHONY: restart run generate migrate
