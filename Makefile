SHELL=/bin/bash -euo pipefail

#Installs dependencies using poetry.
install-python:
	poetry install

#Installs dependencies using npm.
install-node:
	npm install --legacy-peer-deps
	cd sandbox && npm install --legacy-peer-deps

#Configures Git Hooks, which are scripts that run given a specified event.
.git/hooks/pre-commit:
	cp scripts/pre-commit .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit

#Condensed Target to run all targets above.
install: install-node install-python .git/hooks/pre-commit

#Referenced within readme
install-hooks: .git/hooks/pre-commit

#Run the npm linting script (specified in package.json). Used to check the syntax and formatting of files.
lint:
	npm run lint
	find . -name '*.py' -not -path '**/.venv/*' | xargs poetry run flake8

#Removes build/ + dist/ directories
clean:
	rm -rf build
	rm -rf dist

#Creates the fully expanded OAS spec in json
publish: clean
	mkdir -p build
	npm run publish 2> /dev/null

#Runs build proxy script
build-proxy:
	scripts/build_proxy.sh

#Files to loop over in release
_dist_include="pytest.ini poetry.lock poetry.toml pyproject.toml Makefile build/. tests sandbox package.json package-lock.json postman"

#Create /dist/ sub-directory and copy files into directory
release: clean publish build-proxy
	mkdir -p dist
	for f in $(_dist_include); do cp -r $$f dist; done
	cp ecs-proxies-deploy.yml dist/ecs-deploy-sandbox.yml
	cp ecs-proxies-deploy.yml dist/ecs-deploy-internal-qa-sandbox.yml
	cp ecs-proxies-deploy.yml dist/ecs-deploy-internal-dev-sandbox.yml

#################
# Test commands #
#################

TEST_CMD := @APIGEE_ACCESS_TOKEN="$(APIGEE_ACCESS_TOKEN)" \
		PYTHONPATH=./tests \
		poetry run pytest -v \
		--color=yes \
		-n 4 \
		--api-name=communications-manager \
		--proxy-name="$(PROXY_NAME)" \
		-s \
		--reruns 5 \
		--reruns-delay 5 \
		--only-rerun 'AssertionError: Unexpected 429'


PROD_TEST_CMD := $(TEST_CMD) \
		--apigee-app-id="$(APIGEE_APP_ID)" \
		--apigee-organization=nhsd-prod \
		--status-endpoint-api-key="$(STATUS_ENDPOINT_API_KEY)"

.run-sandbox-unit-tests:
	(cd sandbox; rm -rf node_modules; npm install --legacy-peer-deps; npm run test)

.run-postman-sandbox: 
	(rm -rf node_modules; npm install --legacy-peer-deps; npm run sandbox-postman-collection)

.run-locust-tests:
	(sleep 60; \
	poetry run locust -f tests/locust/test_no_errors.py --config .locust.conf; \
	sleep 60; \
	poetry run locust -f tests/locust/test_over_quota.py --config .locust.conf; \
	sleep 60; \
	poetry run locust -f tests/locust/test_over_spike_arrest.py --config .locust.conf;)

#Command to run end-to-end smoketests post-deployment to verify the environment is working
smoketest:
	$(TEST_CMD) \
	--junitxml=smoketest-report.xml \
	-m smoketest

.sandboxtest:
	$(TEST_CMD) \
	--junitxml=test-report.xml \
	--ignore=tests/development \
	--ignore=tests/integration \
	--ignore=tests/mtls \
	-m sandboxtest

sandboxtest: .run-sandbox-unit-tests .run-postman-sandbox .run-locust-tests .sandboxtest

.sandboxtest-prod:
	$(PROD_TEST_CMD) \
	--junitxml=test-report.xml \
	--ignore=tests/development \
	--ignore=tests/integration \
	--ignore=tests/mtls \
	-m sandboxtest

sandboxtest-prod: .run-sandbox-unit-tests .run-postman-sandbox .sandboxtest-prod

test-dev:
	$(TEST_CMD) \
	--junitxml=test-report.xml \
	--ignore=tests/sandbox \
	--ignore=tests/integration \
	-m devtest

test-int:
	$(TEST_CMD) \
	--junitxml=test-report.xml \
	--ignore=tests/sandbox \
	--ignore=tests/development \
	-m inttest

test-prod:
	$(PROD_TEST_CMD) \
	--junitxml=test-report.xml \
	--ignore=tests/sandbox \
	--ignore=tests/development \
	--ignore=tests/integration \
	-m prodtest

test-mtls:
	$(TEST_CMD) \
	--junitxml=test-report.xml \
	--ignore=tests/sandbox \
	--ignore=tests/integration \
	--ignore=tests/development \
	-m mtlstest