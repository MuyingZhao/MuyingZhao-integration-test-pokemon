# Elixir: itrax justfile
# Assists in working with itrax by placing common functionality in one file

# Default variables
report := env_var_or_default("REPORT", "report -m")
service := env_var_or_default("SERVICE", "elixir")

# Default recipe
default: help

# Check if development tools are available
dev-tools-check:
    @if ! command -v docker >/dev/null 2>&1 || ! command -v docker-compose >/dev/null 2>&1; then \
        echo "Error: docker and docker-compose are required"; \
        exit 1; \
    fi

# Check if linting tools are available
lint-tools-check:
    @if ! command -v black >/dev/null 2>&1 || ! command -v isort >/dev/null 2>&1 || ! command -v flake8 >/dev/null 2>&1; then \
        echo "Error: black, isort, and flake8 are required for linting"; \
        exit 1; \
    fi

# Print help information
help:
    @echo "+--------------------------------------------------------------------------------+"
    @echo "| Elixir: itrax                                                                  |"
    @echo "+--------------------------------------------------------------------------------+"
    @echo "|                                                                                |"
    @echo "| Description:                                                                   |"
    @echo "|                                                                                |"
    @echo "| Assists in working with itrax by placing common functionality in one file      |"
    @echo "| much of the usage is combined in few rules that can be customized via          |"
    @echo "| command line arguments.                                                        |"
    @echo "|                                                                                |"
    @echo "| Available commands:                                                            |"
    @echo "|                                                                                |"
    @echo "| help: Prints this message                                                      |"
    @echo "| build: Builds the docker image                                                 |"
    @echo "| start: Runs the application                                                    |"
    @echo "| stop: Stops the application                                                    |"
    @echo "| restart: Restarts the application                                              |"
    @echo "| lint: Lints python code                                                        |"
    @echo "| migrate: Applies the django migrations                                         |"
    @echo "| migrations [args]: Creates the django migrations                               |"
    @echo "| repl: Opens Django shell                                                       |"
    @echo "| shell: Opens bash shell in container                                           |"
    @echo "| test [src] [test-case] [report]: Runs tests with optional parameters           |"
    @echo "| clean: Cleans docker resources and docs                                        |"
    @echo "| docs: Generates documentation                                                  |"
    @echo "| poetry [cmd]: Runs poetry command in container                                 |"
    @echo "| createsuperuser: Creates Django superuser                                      |"
    @echo "| logs: Shows container logs                                                     |"
    @echo "| bizrule: Runs the business rule                                                |"
    @echo "|                                                                                |"
    @echo "| Examples:                                                                      |"
    @echo "|   just build                                                                   |"
    @echo "|   just test . 'itracker.trs.tests' html                                        |"
    @echo "|   just migrations 'myapp'                                                      |"
    @echo "|   just poetry 'show --tree'                                                    |"
    @echo "|                                                                                |"
    @echo "+--------------------------------------------------------------------------------+"

# Build docker image
build force="false": dev-tools-check
    @if [ "{{force}}" = "true" ]; then \
        docker service rm -f {{service}} || true; \
        docker service prune -f || true; \
    fi
    @docker compose build {{service}}

# Start the application
start: dev-tools-check
    @docker compose up {{service}} --remove-orphans -d

# Stop the application
stop: dev-tools-check
    @docker compose stop {{service}}

# Restart the application
restart: stop start

# Lint Python code
lint: lint-tools-check
    #!/usr/bin/env bash
    set -euo pipefail
    files=$(git diff --name-only -- '*.py' 2>/dev/null || true)
    if [ -n "$files" ]; then
        for file in $files; do
            if [ -f "$file" ]; then
                black "$file"
                isort "$file"
                flake8 "$file"
            fi
        done
    else
        echo "No Python files changed"
    fi

# Apply Django migrations
migrate: dev-tools-check
    @docker compose run --rm {{service}} poetry run python ./manage.py migrate

# Create Django migrations
migrations args="": dev-tools-check
    @docker compose run --rm {{service}} poetry run python ./manage.py makemigrations {{args}}

# Open Django shell
repl: dev-tools-check
    @docker compose run --rm {{service}} poetry run python manage.py shell

# Open bash shell in container
shell:
    @docker compose run --rm {{service}} /bin/bash

# Run tests with optional parameters
test src="" test-case="" report-type="": dev-tools-check
    #!/usr/bin/env bash
    set -euo pipefail
    rm -rf coverage
    
    report_arg="{{report}}"
    if [ -n "{{report-type}}" ]; then
        report_arg="{{report-type}}"
    fi
    
    if [ -n "{{test-case}}" ] && [ -n "{{src}}" ]; then
        docker compose run --rm {{service}} poetry run coverage run --source={{src}} --branch ./manage.py test --no-input {{test-case}}
        docker compose run --rm {{service}} poetry run coverage "$report_arg"
    elif [ -n "{{src}}" ]; then
        docker compose run --rm {{service}} poetry run coverage run --source={{src}} --branch ./manage.py test --no-input
        docker compose run --rm {{service}} poetry run coverage "$report_arg"
    elif [ -n "{{test-case}}" ]; then
        docker compose run --rm {{service}} poetry run coverage run --branch ./manage.py test --no-input {{test-case}} --parallel
    else
        docker compose run --rm {{service}} poetry run coverage run --branch ./manage.py test --no-input --parallel
    fi
    
    rm -rf .coverage.* || true

# Clean docker resources
clean-docker:
    @docker volume prune -f
    @docker image prune -f
    @docker system prune -f

# Clean documentation
clean-docs:
    @rm -rf docs/build

# Clean all
clean: clean-docker clean-docs

# Generate documentation
docs: dev-tools-check
    @docker compose run --rm {{service}} poetry run sphinx-apidoc -f -o docs/source/ . ./*/test/*.py ./tests/*.py ./*/migrations/*.py ./*/tests/*.py ./settings/*.py
    @cd docs && make html SERVICE={{service}}

# Run poetry command
poetry cmd: dev-tools-check
    @docker compose run --rm {{service}} poetry {{cmd}}

# Create Django superuser
createsuperuser:
    @docker compose run {{service}} poetry run python manage.py createsuperuser --noinput

# Show container logs
logs: dev-tools-check
    @docker compose logs -f {{service}}

# Run business rule
bizrule:
    @docker compose run {{service}} poetry run python manage.py bizrule
