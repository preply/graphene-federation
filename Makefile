.PHONY: integration-build integration-test dev-setup dev-teardown tests build-artifact-and-deploy-to-images clean-docker

# -------------------------
# Integration testing
# -------------------------

## Build environment for integration tests
integration-build:
	cd integration_tests && docker-compose build

## Run integration tests
integration-test:
	cd integration_tests && docker-compose down && docker-compose up
# cd integration_tests && docker-compose down && docker-compose run --rm tests

integration-test-3-scratch: clean-docker build-artifact-and-deploy-to-images
	@echo "Perform integration test on graphene 3.0.0. We setup it from scratch!"
	cd integration_tests && docker-compose --file="docker-compose-3.yml" build
	cd integration_tests && docker-compose --file="docker-compose-3.yml" down
	cd integration_tests && docker-compose --file="docker-compose-3.yml" up


# -------------------------
# Development and unit testing
# -------------------------

## Install development dependencies
dev-setup:
	docker-compose up -d && docker-compose exec graphene_federation bash

## Run unit tests
tests:
	docker-compose run graphene_federation py.test graphene_federation --cov=graphene_federation -vv

# -------------------------
# Internal
# -------------------------

test-service-a:
	@echo "Checking if service_a, when started, occurs in some hicup. This is used in development, to check if a dn why a container is not running"
	docker rmi --force integration_test_service_a_run_check:latest
	cd integration_tests/service_a && docker build --progress="plain" --tag integration_test_service_a_run_check . && docker run  integration_test_service_a_run_check:latest

build-artifact-and-deploy-to-images:
	@echo "Building graphene-federation wheel file..."
	python3 setup.py bdist_wheel
	@echo "Sending the wheel file to each docker image build folder..."
	cp dist/$(shell ls -t dist/ | egrep .whl | head -n1) integration_tests/service_3_a/
	cp dist/$(shell ls -t dist/ | egrep .whl | head -n1) integration_tests/service_3_b/
	cp dist/$(shell ls -t dist/ | egrep .whl | head -n1) integration_tests/service_3_c/
	cp dist/$(shell ls -t dist/ | egrep .whl | head -n1) integration_tests/service_3_d/

clean-docker:
	@echo "Remove all docker containers and images..."
	docker rmi --force integration_test_service_3_a_run_check:latest
	docker rmi --force integration_test_service_3_b_run_check:latest
	docker rmi --force integration_test_service_3_c_run_check:latest
	docker rmi --force integration_test_service_3_d_run_check:latest
	docker rmi --force integration_tests_service_3_a:latest
	docker rmi --force integration_tests_service_3_b:latest
	docker rmi --force integration_tests_service_3_c:latest
	docker rmi --force integration_tests_service_3_d:latest
	docker rmi --force graphene-federation_graphene_federation
	docker rmi --force integration_tests_federation_3
	docker rmi --force integration_tests_tests_3
	docker rmi --force integration_tests_service_a:latest
	docker rmi --force integration_tests_service_b:latest
	docker rmi --force integration_tests_service_c:latest
	docker rmi --force integration_tests_service_d:latest
	docker rmi --force integration_tests_service_a_1:latest
	docker rmi --force integration_tests_service_b_1:latest
	docker rmi --force integration_tests_service_c_1:latest
	docker rmi --force integration_tests_service_d_1:latest
	docker rmi --force integration_tests_federation
	docker rmi --force integration_tests_tests
	docker rmi --force federation


test-service-3-a: build-artifact-and-deploy-to-images
	@echo "Checking if service_3_a, when started, occurs in some hiccups..."
	docker rmi --force integration_test_service_3_a_run_check:latest
	cd integration_tests/service_3_a && docker build --progress="plain" --tag integration_test_service_3_a_run_check . && docker run integration_test_service_3_a_run_check:latest
