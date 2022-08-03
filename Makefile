build:
	cd integration_tests && docker-compose build

mypy:
	mypy graphene_federation

test:
	cd integration_tests && docker-compose down && docker-compose run --rm tests
