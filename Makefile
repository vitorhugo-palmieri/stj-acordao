image:
	docker build -t crawler-juris-stj-acordao .

clean:
	docker kill $$(docker ps -q)
	docker rm $$(docker ps -a -q)

remove-containers:
	docker rm $$(docker ps -a -q)

down:
	docker-compose down

remove-debug-files:
	rm -rf tests/files/debug/

run-unit-tests: image
	docker run --entrypoint ./scripts/run-unit-tests.sh -v $$(pwd)/tests/files/tests_files/:/app/tests/files/tests_files/ crawler-juris-stj-acordao

sudo run-integration-tests: image remove-debug-files
	docker-compose run --entrypoint ./scripts/run-integration-tests.sh crawler-juris-stj-acordao

shell: image
	docker-compose run --entrypoint /bin/bash crawler-juris-stj-acordao

run: image
	docker-compose up