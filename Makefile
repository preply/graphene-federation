build:
	cd integration_tests && docker-compose build

test:
	cd integration_tests && docker-compose down && docker-compose run --rm tests
