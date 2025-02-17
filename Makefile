SHELL=/bin/bash -euo pipefail

#Installs dependencies using poetry.
install-python:
	poetry install

#Installs dependencies using npm.
install-node:
	npm install --legacy-peer-deps
	cd sandbox && npm install --legacy-peer-deps

#Configures Git Hooks, which are scripts that run given a specified event.
git/hooks/pre-commit:
	cp scripts/pre-commit .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit

#Condensed Target to run all targets above.
install: install-node install-python git/hooks/pre-commit

#Referenced within readme
install-hooks: .git/hooks/pre-commit

#Run the npm linting script (specified in package.json). Used to check the syntax and formatting of files.
lint: .check-licenses .ensure-test-documentation-validity .lint-js .lint-python
	npm run lint

static-analysis:
	npm run static-analysis

#Removes build/ + dist/ directories
clean:
	rm -rf build
	rm -rf dist

#Creates the fully expanded OAS spec in json
publish: clean
	mkdir -p build
	npm run publish

#Runs build proxy script
build-proxy:
	scripts/build_proxy.sh

.ensure-test-documentation-validity:
	cd tests/docs && ./build-docs.sh --verify && cd ../../

build-test-documentation:
	cd tests/docs && ./build-docs.sh --build-only && cd ../../

# Lint JavaScript files
.lint-js:
	node_modules/.bin/eslint sandbox/

# Lint Python files
.lint-python:
	find . -name '*.py' -not -path '**/.venv/*' | xargs poetry run flake8

#Files to loop over in release
_dist_include="pytest.ini poetry.lock poetry.toml pyproject.toml Makefile build/. tests sandbox package.json package-lock.json postman scripts"

#Create /dist/ sub-directory and copy files into directory
release: clean publish build-proxy
	mkdir -p dist
	for f in $(_dist_include); do cp -r $$f dist; done
	cp ecs-proxies-deploy.yml dist/ecs-deploy-sandbox.yml
	cp ecs-proxies-deploy.yml dist/ecs-deploy-internal-qa-sandbox.yml
	cp ecs-proxies-deploy.yml dist/ecs-deploy-internal-dev-sandbox.yml

#Serve the OAS specification
serve:
	npm run publish
	(sleep 5; python3 -m webbrowser http://127.0.0.1:5000) &
	npm run serve

#Check dependencies for licensing issues
.check-licenses:
	npm run check-licenses
	scripts/check_python_licenses.sh
	cd sandbox && npm run check-licenses

check-licenses: .check-licenses

#################
# Test commands #
#################

TEST_CMD := @APIGEE_ACCESS_TOKEN="$(APIGEE_ACCESS_TOKEN)" \
		PYTHONPATH=./tests \
		poetry run pytest -vv \
		--color=yes \
		-n 4 \
		--api-name=communications-manager \
		--proxy-name="$(PROXY_NAME)" \
		-s \
		--reruns 5 \
		--reruns-delay 5 \
		--only-rerun 'AssertionError: Unexpected 429' \
		--only-rerun 'AssertionError: Unexpected 504' \
		--only-rerun 'AssertionError: Unexpected 401' \
		--only-rerun 'AssertionError: Unexpected 502' \
	    --junitxml=test-report.xml

PERFTEST_CMD := @APIGEE_ACCESS_TOKEN="$(APIGEE_ACCESS_TOKEN)" \
		PYTHONPATH=./tests \
		poetry run pytest -vv \
		--color=yes \
		-n 1 \
		--api-name=communications-manager \
		--proxy-name="$(PROXY_NAME)" \
		-s \
		--reruns 8 \
		--reruns-delay 30 \
	    --junitxml=perftest-report.xml

PROD_TEST_CMD := @APIGEE_ACCESS_TOKEN="$(APIGEE_ACCESS_TOKEN)" \
		PYTHONPATH=./tests \
		poetry run pytest -vv \
		--color=yes \
		-n 1 \
		--api-name=communications-manager \
		--proxy-name="$(PROXY_NAME)" \
		-s \
		--reruns 5 \
		--reruns-delay 5 \
		--only-rerun 'AssertionError: Unexpected 429' \
		--only-rerun 'AssertionError: Unexpected 504' \
		--apigee-app-id="$(APIGEE_APP_ID)" \
		--apigee-organization=nhsd-prod \
		--status-endpoint-api-key="$(STATUS_ENDPOINT_API_KEY)" \
		--junitxml=test-report.xml

.run-sandbox-unit-tests:
	(cd sandbox; rm -rf node_modules; npm install --legacy-peer-deps; npm run test)

.run-postman-sandbox:
	(rm -rf node_modules; npm install --legacy-peer-deps; npm run sandbox-postman-collection)

.run-postman-int:
	(rm -rf node_modules; npm install --legacy-peer-deps; \
	npm run integration-postman-collection)

sandbox-postman-test: .run-postman-sandbox

int-postman-test: .run-postman-int

zap-security-scan:
	(rm -rf node_modules; npm install --legacy-peer-deps; npm run zap-security-scan)

.internal-sandbox-test:
	$(TEST_CMD) \
	tests/sandbox \
	-m sandboxtest

internal-sandbox-test: .run-sandbox-unit-tests .run-postman-sandbox .internal-sandbox-test

.prod-sandbox-test:
	$(PROD_TEST_CMD) \
	tests/sandbox \
	-m sandboxtest

prod-sandbox-test: .run-sandbox-unit-tests .run-postman-sandbox .prod-sandbox-test

.internal-dev-test:
	$(TEST_CMD) \
	tests/development \
	-m devtest

.internal-dev-perftest:
	$(PERFTEST_CMD) \
	tests/development \
	-m devperftest

internal-dev-test: .internal-dev-test

internal-dev-test-nightly: .internal-dev-test .internal-dev-perftest

internal-qa-test:
	$(TEST_CMD) \
	tests/development \
	-m "not devtestonly and devtest or uattest"

.integration-test:
	$(TEST_CMD) \
	tests/integration \
	-m inttest

integration-test: .run-postman-int .integration-test

.production-test:
	$(PROD_TEST_CMD) \
	tests/production \
	-m prodtest

production-test: .production-test

mtls-test-dev:
	$(TEST_CMD) \
	tests/mtls \
	-m "mtlstest and devtest or uattest"

mtls-test-prod:
	$(TEST_CMD) \
	tests/mtls \
	-m "mtlstest and inttest or prodtest"

e2e-test-internal-dev:
	$(TEST_CMD) \
	tests/end_to_end \
	-m "e2e and devtest"

e2e-test-uat:
	$(TEST_CMD) \
	tests/end_to_end \
	-m "e2e and uattest"

test:
	$(TEST_CMD) \
	tests/api \
	-m "test"