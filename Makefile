

### <summary>
### Build a Python 3 image for instlaling development dependencies and local
### development.
### </summary>
.PHONY: build
build:
	@docker compose \
		-f docker-compose.yaml \
		build


.PHONY: build.all
build.all: build build.integration-tests


### <summary>
### Build both Graphene 2.x and Graphene 3.x integration test environments.
### </summary>
.PHONY: build.integration-tests
build.integration-tests: build.integration-tests.graphene2 build.integration-tests.graphene3


### <summary>
### Build the images for integration testing on Graphene 2.x
### </summary>
.PHONY: build.integration-tests.graphene2
build.integration-tests.graphene2:
	@echo "Building integration test environment for: Graphene 2.x"
	@cd integration_tests/graphene-2.x && docker compose \
		-f docker-compose.yaml \
		build


### <summary>
### Build the images for integration testing on Graphene 3.x
### </summary>
.PHONY: build.integration-tests.graphene3
build.integration-tests.graphene3:
	@echo "Building integration test environment for: Graphene 3.x"
	@cd integration_tests/graphene-3.x && docker compose \
		-f docker-compose.yaml \
		build


### <summary>
### 
### </summary>
.PHONY: clean
clean: docker.clean


.PHONY: clean.full
clean: .remove-integration-images clean


.PHONY: docker.clean
docker.clean:
	@echo "> Perform docker system prune..."
	@docker system prune -f


.PHONY: shell.dev
shell.dev:
	@docker compose -f docker-compose.yaml run graphene_federation /bin/bash 


.PHONY: shell.integration.graphene2
shell.integration.graphene2:
	@docker compose -f integration_tests/graphene-2.x/docker-compose.yaml run service /bin/sh


.PHONY: stop
stop:
	@echo "Stopping all containers..."
	@docker compose -f integration_tests/graphene-2.x/docker-compose.yaml down
	@docker compose -f integration_tests/graphene-3.x/docker-compose.yaml down


### <summary>
### Run Graphene unit tests.
### </summary>
.PHONY: test
test:
	@docker compose run graphene_federation pytest graphene_federation --cov=graphene_federation -vv


## Run unit tests
.PHONY: test.all
test.all: build test build.integration-tests test.integration


## Run integration tests
.PHONY: test.integration
test.integration: test.integration.graphene2 test.integration.graphene3


.PHONY: test.integration.graphene2
test.integration.graphene2:
	@echo "Running integration tests for: Graphene 2"
	@docker compose -f integration_tests/graphene-2.x/docker-compose.yaml down
	@docker compose -f integration_tests/graphene-2.x/docker-compose.yaml up -d
	@docker compose -f integration_tests/graphene-2.x/docker-compose.yaml run --rm test_runner


.PHONY: test.integration.graphene3
test.integration.graphene3:
	@echo "Running integration tests for: Graphene 3"
	@docker compose -f integration_tests/graphene-3.x/docker-compose.yaml down
	@docker compose -f integration_tests/graphene-3.x/docker-compose.yaml up -d
	@docker compose -f integration_tests/graphene-3.x/docker-compose.yaml run --rm test_runner


# .PHONY: test.integration.graphene3.clean
# test.integration.graphene3.clean: clean .prepare-graphene3-integration-tests build.integration-tests.graphene3 test.integration.graphene3


# test-service-a:
# 	@echo "Checking if service_a, when started, occurs in some hicup. This is used in development, to check if a dn why a container is not running"
# 	docker rmi --force integration_test_service_a_run_check:latest
# 	cd integration_tests/service_a && docker build --progress="plain" --tag integration_test_service_a_run_check . && docker run  integration_test_service_a_run_check:latest


# test-service-3-a: .prepare-graphene3-integration-tests
# 	@echo "Checking if service_3_a, when started, occurs in some hiccups..."
# 	docker rmi --force integration_test_service_3_a_run_check:latest
# 	cd integration_tests/service_3_a && docker build --progress="plain" --tag integration_test_service_3_a_run_check . && docker run integration_test_service_3_a_run_check:latest



### <summary>
###
### </summary>
.PHONY: .remove-integration-images
.remove-integration-images:
	@echo "Remove all docker containers and images..."
# Remove all of the Graphene 2 images
	@echo "Removing Graphene 2 images..."
	@docker rmi --force graphene_federation/integration-tests/service:graphene-2
	@docker rmi --force graphene_federation/integration-tests/federation:graphene-2
	@docker rmi --force graphene_federation/integration-tests/test_runner:graphene-2
# Remove all of the Graphene 3 images
	@echo "Removing Graphene 3 images..."\
	@docker rmi --force graphene_federation/integration-tests/service:graphene-3
	@docker rmi --force graphene_federation/integration-tests/federation:graphene-3
	@docker rmi --force graphene_federation/integration-tests/test_runner:graphene-3


# .PHONY: .prepare-graphene3-integration-tests
# .prepare-graphene3-integration-tests:
# 	@echo "Building graphene-federation wheel file..."
# 	@python3 setup.py bdist_wheel
# 	@echo "Sending the wheel file to each docker image build folder..."
# 	@cp dist/$(shell ls -t dist/ | egrep .whl | head -n1) integration_tests/graphene-3.x/service_a/
# 	@cp dist/$(shell ls -t dist/ | egrep .whl | head -n1) integration_tests/graphene-3.x/service_b/
# 	@cp dist/$(shell ls -t dist/ | egrep .whl | head -n1) integration_tests/graphene-3.x/service_c/
# 	@cp dist/$(shell ls -t dist/ | egrep .whl | head -n1) integration_tests/graphene-3.x/service_d/

