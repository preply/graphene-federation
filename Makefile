# -------------------------
# Integration testing
# -------------------------

.PHONY: integration-build ## Build environment for integration tests
integration-build:
	cd integration_tests && docker-compose build

.PHONY: integration-test ## Run integration tests
integration-test:
	cd integration_tests && docker-compose down && docker-compose run --rm tests

# -------------------------
# Development and unit testing
# -------------------------

.PHONY: dev-setup ## Install development dependencies
dev-setup:
	docker-compose up -d && docker-compose exec graphene_federation bash

.PHONY: dev-teardown ## Uninstall development dependencies
dev-teardown:
	docker-compose down --rmi="all"
	cd integration_tests && docker-compose down --rmi="all"
	cd integration_tests && docker-compose run --rm tests

.PHONY: tests ## Run unit tests
tests:
	docker-compose run graphene_federation py.test graphene_federation --cov=graphene_federation -vv

