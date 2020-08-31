build:
	cd integration_tests && \
	echo service_[a-d] | xargs -n 1 cp -r service_common/* && \
	docker-compose build

test:
	cd integration_tests && docker-compose down && docker-compose run --rm tests
