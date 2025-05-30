# Communications Manager API

![Build](https://github.com/NHSDigital/communications-manager-api/workflows/Build/badge.svg?branch=release)

This is the RESTful API for the [*NHS Notify Service*](https://digital.nhs.uk/developer/api-catalogue/nhs-notify).

It includes:

* `specification/` - This [Open API Specification](https://swagger.io/docs/specification/about/) describes the endpoints, methods and messages exchanged by the API. Use it to generate interactive documentation; the contract between the API and its consumers.
* `sandbox/` - This NodeJS application implements a mock implementation of the service. Use it as a back-end service to the interactive documentation to illustrate interactions and concepts. It is not intended to provide an exhaustive/faithful environment suitable for full development and testing.
* `scripts/` - Utilities helpful to developers of this specification.
* `proxies/` - Live (connecting to another service) and sandbox (using the sandbox container) Apigee API Proxy definitions.
* `azure/` - Azure Devops pipeline definitions.
* `zap/` - Zap security scan configuration.
* `tests/` - Integration test suites.
* `postman/` - Postman collections.
* `docs/` - [Documentation for the project](docs/index.md)

Consumers of the API will find developer documentation on the [NHS Notify API entry](https://digital.nhs.uk/developer/api-catalogue/nhs-notify).

This repo does not include the Communications Manager back-end that is not currently open source.

## Contributing

Contributions to this project are welcome from anyone, providing that they conform to the [guidelines for contribution](CONTRIBUTING.md) and the [community code of conduct](CODE_OF_CONDUCT.md).

### Licensing

This code is dual licensed under the MIT license and the OGL (Open Government License). Any new work added to this repository must conform to the conditions of these licenses. In particular this means that this project may not depend on GPL-licensed or AGPL-licensed libraries, as these would violate the terms of those libraries' licenses.

The contents of this repository are protected by Crown Copyright (C).

## Development

N.B. that some functionality requires environment variables to be set, these are described lower down in the readme.

Windows users should install [Windows Subsystem for Linux (WSL)](https://learn.microsoft.com/en-us/windows/wsl/install). Any distro is fine, though ubuntu/debian are recommended.

### Requirements

* make
* [nvm](https://github.com/nvm-sh/nvm)
* [pyenv](https://github.com/pyenv/pyenv)
* [poetry](https://github.com/python-poetry/poetry)
* Java 8+
* [get\_token](https://docs.apigee.com/api-platform/system-administration/auth-tools#install)

### Install

```
$ nvm install && nvm use
$ pyenv install -s && pyenv shell && pyenv local
$ make install
```

#### Updating hooks

You can install some pre-commit hooks to ensure you can't commit invalid spec changes by accident. These are also run in CI, but it's useful to run them locally too.

```
$ make install-hooks
```

There is a specific pre-commit hook for secret scanning. Documentation on how to enable this can be found [here](nhsd-git-secrets/README.md).

### Environment Variables

Various scripts and commands rely on environment variables being set. These are documented with the commands.

There is an example `.env` file [here](https://github.com/NHSDigital/communications-manager-api/blob/release/example.env).

To create your own version:

```
$ cp example.env .env
```

To use your local `.env` file make sure to source it:

```
$ source .env
```

As a reminder: environment variable changes from the `.env` file take place only when the workspace is reloaded (e.g. through a new cli or `direnv allow`)

### Make commands

There are `make` commands that alias some of this functionality:

* `lint` -- Lints the spec and code
* `publish` -- Outputs the specification as a **single file** into the `build/` directory
* `serve` -- Serves a preview of the specification in human-readable format - your browser will automatically open the documentation
* `build-test-documentation` -- Builds the test documentation that is checked into the repository under `docs/tests`

## Testing

The tests written in this repository target the NHS Notify API. The types of testing this repository include are:

* Unit tests
* Integration tests
* End to End tests
* Zap security scan tests
* Postman collection tests

For details on test cases covered in the Integration and End-to-End test suites, see the [test documentation](docs/tests/index.md).

### Set Up

#### Python
Before running tests, you need to set up your local environment. Use the `poetry install` command to install dependencies and populate the `.venv` directory.

```
poetry install
```

Activate the virtual environment with the following command:

```
source .venv/bin/activate
```

#### Authentication

Our API integration tests support two authentication methods:

* __Bearer Token Authentication (via API key and private key)__ - Used for common integration tests across all environments.
* __Apigee Authentication (using pytest-nhsd-apim)__ - Used for some internal-dev and dev tests and all internal-dev-sandbox and sandbox tests.

#### Bearer Token Authentication

>**Notice:** This section contains the handling of secrets. As a reminder, secrets should only be shared via secure methods (e.g. NHS Mail) and MUST NOT be committed to source control

##### Set the Environment

To be able to generate bearer token authentication for tests you need to declare the `API_ENVIRONMENT` environment variable, e.g.:

```
export API_ENVIRONMENT=internal-dev
```

Available values for `API_ENVIRONMENT` include:
* `internal-dev`
* `internal-dev-test-1`
* `internal-qa`
* `int`
* `prod`

This defines the scope of tests that will be executed and the Apigee App/Product  that will be used to service requests.

The authentication process uses an API and private key pairing for the application defined by the `API_ENVIRONMENT`

##### API Key

To define the API Key, the following envars are used:

|Environment|API Key Variable|Private Key Variable|
|-----------|----------------|--------------------|
|internal-dev, internal-qa|`NON_PROD_API_KEY`|`NON_PROD_PRIVATE_KEY`|
|internal-dev-test-1|`NON_PROD_API_KEY_TEST_1`|`NON_PROD_PRIVATE_KEY`|
|int|`INTEGRATION_API_KEY`|`INTEGRATION_PRIVATE_KEY`|
|prod|`PRODUCTION_API_KEY`|`PRODUCTION_PRIVATE_KEY`|

To find the values for the `*_API_KEY` values:
* Identify the correct envar for your `API_ENVIRONMENT` from the table above
* Navigate to the Apigee App that will serve that environment e.g. `Comms-manager-local`
* Copy the value of the `Key` found in the credentials section to your envar in `.env`

In addition the `API_KEY` envar is also used and should use the same value.

##### Private Key

The value of the `*_PRIVATE_KEY` envars are a *file path* to the location of a private key file.

The keys are held securely within the Management Account - talk to existing team members for more information on sourcing and configuring these values

>__Ensure these variables are set and sourced in your .env file before running tests.__

#### Generate An Apigee Access Token

To generate authentication using Apigee, you must have access to an Apigee account and use `get_token` via the command line and generate an Apigee access token. 

__Tokens expire once per day and require refreshing.__

* Install [get\_token](https://docs.apigee.com/api-platform/system-administration/auth-tools#install)
* Run the following command and log in with your Apigee credentials when prompted:
```
export APIGEE_ACCESS_TOKEN=$(SSO_LOGIN_URL=https://login.apigee.com get_token)
```
* If your token does not refresh, try clearing the cache:
```
export APIGEE_ACCESS_TOKEN=$(SSO_LOGIN_URL=https://login.apigee.com get_token --clear-sso-cache)
```

#### Set Proxy Name
Set the `PROXY_NAME` environment variable to specify the environment for test execution. You can find the proxy name by logging into [Apigee](https://apigee.com/edge), navigating to 'API Proxies' and searching for 'communications-manager'.

```
export PROXY_NAME=communications-manager-internal-dev
```

Available values for `PROXY_NAME` include:

* `communications-manager-internal-dev`
* `communications-manager-internal-dev-sandbox`
* `communications-manager-pr-{num}`
* `communications-manager-pr-{num}-sandbox`

### Set Up End to End Tests

If you are running the end to end tests you will need to set the following environment variables:
* `GUKN_API_KEY` - Gov UK Notify API Key for the internal dev environment, this value can be found in AWS parameter store under /comms/govuknotify/internal-dev/api_key in the 'NHS Digital Comms Mgr Dev' account
* `UAT_GUKN_API_KEY` - Gov UK Notify API Key for the UAT environment, this value can be found in AWS parameter store under /comms/govuknotify/uat/api_key in the 'NHS Digital Comms Mgr Test' account
* `UAT_NHS_APP_USERNAME` - NHS App username, this value can be found [here](https://nhsd-confluence.digital.nhs.uk/display/RIS/NHS+Notify+%7C+NHS+App+Test+User+and+Environments)
* `UAT_NHS_APP_PASSWORD` - NHS App password, this value can be found [here](https://nhsd-confluence.digital.nhs.uk/display/RIS/NHS+Notify+%7C+NHS+App+Test+User+and+Environments)
* `UAT_NHS_APP_OTP` - NHS App one time passcode, this value can be found [here](https://nhsd-confluence.digital.nhs.uk/display/RIS/NHS+Notify+%7C+NHS+App+Test+User+and+Environments)

__When exporting values on your local machine, be sure to escape special characters i.e: `\! \# \$`__

### Running Tests

#### Unit Tests

These tests live within the `/sandbox` folder and can be executed by:

```
$ cd sandbox
$ npm i
$ npm run test
```

Basic test coverage is enforced through NYC - this is configured within `/sandbox/.nycrc.json`. If the tests fail or coverage does not meet the targets set out in the NYC configuration then the unit tests will fail.

#### Integration tests

Integration tests live within the `tests/api/` directory and use pytest markers to call out tests for a specific environment.

* `all` - can be ran against all environments
* `devtest` - can be ran against the internal-dev or internal-qa environments
* `devtestonly` - can only be ran against internal-dev environment
* `devperftest` - can only be ran on internal-dev - separate from the standard internal-dev test run on the nightly pipeline
* `uattest` - can only be ran on internal-qa environment
* `inttest` - can be ran against the int environment
* `prodtest` - can be ran against the production environment

#### Running with make

Tests can be ran via make command.

```
make test
```

A full list of available commands can be found in the Makefile. 

The table below lists common make commands used for testing:

|Environment|Command|Description|
|-----------|-------|-----------|
|internal-dev-sandbox|`make internal-sandbox-test`|Runs sandbox unit tests, sandbox postman tests and sandbox integration tests against internal-dev-sandbox|
|internal-dev|`make internal-dev-test`|Runs integration tests against internal-dev|
|internal-dev|`make e2e-test-internal-dev`|Runs end to end tests against internal-dev|
|internal-qa|`make internal-qa-test`|Runs integration tests against internal-qa|
|internal-qa|`make e2e-test-uat`|Runs end to end tests against internal-qa|
|int|`make integration-test`|Runs integration tests against int|
|prod|`make production-test`|Runs integration tests against prod|


#### Running with poetry

Tests can be ran via poetry command. To run a poetry test run the following command in the root folder

```
PYTHONPATH=./tests poetry run pytest -v -m <TAG> <path to file> --api-name=communications-manager --proxy-name=$PROXY_NAME --apigee-access-token=$APIGEE_ACCESS_TOKEN -n 4 --only-rerun 'AssertionError: Unexpected 429' --reruns 5 --reruns-delay 5 --color=yes --junitxml=test-report.xml -k <test name>
```

You can use poetry to specify a specific directory or test to run without having to run the full test suite. 

The table below lists the arguments used in a poetry test and how they are used to specify a test:

|Argument|Description|
|--------|-----------|
|`PYTHONPATH=./tests`|Sets the root directory of the tests|
|`poetry run pytest`|Runs pytest through poetry|
|`-v`|Marks logs as verbose (Optional)|
|`-m <TAG>`|Specifies tag name (Optional)|
|`<relative path to file>`|Targets a specific file to run tests for, useful when developing new tests (Optional)|
|`--api-name=communications-manager`|Specifies api name|
|`--proxy-name=$PROXY_NAME`|Retrieves the PROXY_NAME environment variable and sets it to the proxy-name argument|
|`--apigee-access-token=$APIGEE_ACCESS_TOKEN`|Retrieves the APIGEE_ACCESS_TOKEN environment variable and sets it to the apigee-access-token argument|
|`-n 4`|The number of parallel runners the tests are executed on|
|`--only-rerun 'AssertionError: Unexpected 429`|The condition to retry on test failure|
|`--reruns 5`|The number of times a test is attempted if it fails on a specified condition|
|`--reruns-delay 5`|The number of seconds to wait before a test is retried|
|`--color=yes`|Displays logs in an easy to read format (Optional)|
|`--junitxml=test-report.xml`|Sets the output of the test run, this will be located in the python path root directory for the tests|
|`-k`|specify a specific test to run|


#### Zap security scanner

You can run the Zap security scanner using the `zap-security-scan` make command:

```
$ make zap-security-scan
```

The project uses the [Zap automation framework](https://www.zaproxy.org/docs/automate/automation-framework/). The configuration for this is held in the `zap/` folder.

#### Postman collection tests

You can test the postman collections by using the `postman-test` make command:

```
$ make postman-test
```

The postman collections can be found in the `postman/` folder.

## Caveats

#### Apigee Portal

The Apigee portal will not automatically pull examples from schemas, you must specify them manually.

### Detailed folder walk through

#### `/.github`:

This folder contains templates that can be customised for items such as opening pull requests or issues within the repo

`/.github/workflows`: This folder contains templates for github action workflows such as:

* `pr-lint.yaml`: This workflow links PRs to the relevant Jira ticket
* `continuous-integration.yml`: This workflow handles the publishing of new releases
* `build.yml`: This workflow builds and lints the project, its status drives the badge in the readme

#### `/azure`:

Contains templates defining Azure Devops pipelines. By default the following pipelines are available:

*  `azure-build-pipeline.yml` - Assembles the contents of the repository into a single file ("artifact") on Azure Devops and pushes any containers to the APIM Docker registry. By default this pipeline is enabled for all branches apart from master.
* `azure-pr-pipeline.yml` - Deploys ephemeral versions of the proxy/spec to Apigee (and docker containers on AWS) to internal environments. You can run automated and manual tests against these while you develop. By default this pipeline will deploy to internal-dev, but the template can be amended to add other environments as required.
* `azure-release-pipeline.yml` - Deploys the long-lived version of the pipeline to internal and external environments - this is run on releases and on merges into release
* `nightly-int-dev-pipeline.yml` - Runs the `dev-test` suite of tests against the internal-dev environment every night. Failures can be subscribed to on the azure devops CI.
* `periodic-mtls-pipeline.yml` - Runs the `mtls-test` suite of tests against the internal-dev, integration and production load balancer targets to ensure that mutual TLS is being enforced. This pipeline runs every 10 minutes. Failures can be subscribed to on the azure devops CI.

`/azure/templates`: Contains our re-usable actions, including:
* `run-tests.yml`: The standard pipeline template for running our test suites.

#### `/proxies`:

This folder contains files relating to the Communications Manager Apigee API proxy.

There are 2 proxy folders `/live` and `/sandbox`. The `/live` folder contains the configuration that is specific to all none sandbox proxy instances - `/sandbox` contains the sandbox proxy definition.

The `/shared` folder contains policies, partials and resources that are used within both the live and sandbox proxies. These are used to build the live and sandbox proxies, the process for which is set out in the `/scripts/build_proxy.sh` script. The build process allows the use of jinja2 template commands, with the following configured wrapper values:

* `[% ... %]` - block start and end
* `[[ ... ]]` - variable start and end

The proxy has been documented [here](docs/proxies.md).

#### `/sandbox`:

This folder contains the sandbox mock application. This is a basic express application that mirrors the responses from the existing backend service.

The sandbox mock contains the following npm run commands:

* `start` - run the sandbox mock
* `start:hotreload` - runs the sandbox mock with hotreloading enables
* `test` - run the sandbox mock unit test suite

#### `/scripts`:

Contains useful scripts that are used throughout the project, these are:

* `build_proxy.sh` - builds the final live and sandbox proxy configurations
* `calculate_version.py` - scans git history to determine the version of the API
* `check_python_licenses.sh` - scans python libraries for license issues
* `generate_bearer_token.py` - generates a bearer token using the env vars `API_KEY` and `API_ENVIRONMENT`
* `pre-commit` - the pre-commit script
* `process_imports.py` - processes the imports for building the proxies, called by `build_proxy.sh`
* `run_zap.sh` - runs the zap security scanner
* `set_version.py` - sets the version number within the OAS spec file during build time
* `sync_postman_collections.sh` - synchronises the postman collections into the repo

#### `/specification`:

This folder contains the Open API specification for the Communications Manager API. The specification is broken down into multiple files to aid readability and reuse.

#### `/tests`:

The integration test suite, see the previous testing section for more information on running the test suites.

#### `ecs-proxies-containers.yml ` and `ecs-proxies-deploy.yml`:

These files define the sandbox mock application container deployment to ECS:

* `ecs-proxies-containers.yml`: The path to a container's Dockerfile is defined here.
* `ecs-proxies-deploy.yml` : Configuration for the ECS deployment.

For more information about deploying ECS containers see the [API Producer Zone confluence](https://nhsd-confluence.digital.nhs.uk/display/APM/Developing+ECS+proxies#DevelopingECSproxies-Buildingandpushingdockercontainers).

#### `manifest_template.yml`:

This defines the Apigee API, including:

* service name
* display name on the NHS onboarding portal
* description of the API
* environments supported by the API
* rate limiting & quotas

#### Package management:

This template uses poetry for python dependency management, and uses these files: poetry.lock, poetry.toml, pyproject.toml.

Node dependencies of this template project and some npm scripts are listed in: package.json, package-lock.json.

#### Postman:

Included in this repo are postman collections that allows the user to interact with the sandbox and integration APIs.

To use the collections:

* Download the json files located in the postman directory
* Import the files into postman
* Select a target environment in postman
* Set the environment variables 'api-key' and 'private-key' for the desired environment (this does not apply for sandbox)
* Run the collection

The collections must be kept in sync manually, this is done by setting the `INTEGRATION_COLLECTION_API_KEY` and `SANDBOX_COLLECTION_API_KEY` environment variables then running the `scripts/sync_postman_collections.sh` script.

## Releasing


Our release process is [documented here](https://nhsd-confluence.digital.nhs.uk/pages/viewpage.action?pageId=789753975).