# Communications Manager API

![Build](https://github.com/NHSDigital/communications-manager-api/workflows/Build/badge.svg?branch=release)

This is the RESTful API for the [*Communications Manager Service*](https://digital.nhs.uk/developer/api-catalogue/communications-manager).

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

Consumers of the API will find developer documentation on the [Communications Manager API entry](https://digital.nhs.uk/developer/api-catalogue/communications-manager).

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

### Make commands

There are `make` commands that alias some of this functionality:

* `lint` -- Lints the spec and code
* `publish` -- Outputs the specification as a **single file** into the `build/` directory
* `serve` -- Serves a preview of the specification in human-readable format - your browser will automatically open the documentation
* `build-test-documentation` -- Builds the test documentation that is checked into the repository under `docs/tests`

### Testing

You can view the documentation about all of the test cases that are covered with the test suites in the [test documentation](docs/tests/index.md).

There are:

* Sandbox mock unit tests
* Integration tests
* Zap security scan tests
* Postman collection tests

#### Node unit tests

These tests live within the `/sandbox` folder and can be executed by:

```
$ cd sandbox
$ npm i
$ npm run test
```

Basic test coverage is enforced through NYC - this is configured within `/sandbox/.nycrc.json`. If the tests fail or coverage does not meet the targets set out in the NYC configuration then the unit tests will fail.

#### Integration tests - dynamic environments

There are several integration test suites configured within the `pytest.ini`, two of these are for testing our dynamic environments - `internal-dev`, `internal-qa` and `sandbox`:

* sandboxtest
* devtest

##### Python setup

Before running any tests you will need to build up your local environment to have access to the resources you need to successfully run tests, to do this run the `poetry install` command. This will populate the .venv directory. To source the .venv file, run source .venv/bin/activate in your shell type of choice:

* bash/zsh: `source .venv/bin/activate`
* csh: `source .venv/bin/activate.csh`
* fish: `source .venv/bin/activate.fish`
* nushell: `source .venv/bin/activate.nu`
* powershell: `. .venv/bin/activate.ps1`

##### Set up

Before running the integration tests against dynamic environments you need to generate an [apigee access token](https://nhsd-confluence.digital.nhs.uk/display/APM/Test+Utils+2.0%3A+Running+tests). To generate a token run the following command, you will then be prompted to log in to apigee with your username, password and MFA code.

```
export APIGEE_ACCESS_TOKEN=$(SSO_LOGIN_URL=https://login.apigee.com get_token)
```

Set the `PROXY_NAME` environment variable to the environment you want to run the tests on. You can find the proxy name by logging into [Apigee](https://apigee.com/edge), navigating to 'API Proxies' and searching for 'communications-manager', this will show you a list of available proxies, eg:

* communications-manager-internal-dev
* communications-manager-internal-dev-sandbox
* communications-manager-pr-{num}
* communications-manager-pr-{num}-sandbox

If you are running the end to end tests you will need to set the following environment variables:
* `GUKN_API_KEY` - Gov UK API Key for the internal dev environment, this value can be found in AWS parameter store under /comms/govuknotify/internal-dev/api_key
* `UAT_GUKN_API_KEY` - Gov UK API Key for the UAT environment, this value can be found in AWS parameter store under /comms/govuknotify/uat/api_key
* `UAT_NHS_APP_USERNAME` - NHS App username, this value can be found [here](https://nhsd-confluence.digital.nhs.uk/display/RIS/NHS+Notify+%7C+NHS+App+Test+User+and+Environments)
* `UAT_NHS_APP_PASSWORD` - NHS App password, this value can be found [here](https://nhsd-confluence.digital.nhs.uk/display/RIS/NHS+Notify+%7C+NHS+App+Test+User+and+Environments)
* `UAT_NHS_APP_OTP` - NHS App one time passcode, this value can be found [here](https://nhsd-confluence.digital.nhs.uk/display/RIS/NHS+Notify+%7C+NHS+App+Test+User+and+Environments)

**Note**
When exporting values on your local machine, be sure to escape special characters i.e: `\! \# \$`

##### Running with make

In the root folder run the following command:

* devtest - `make internal-dev-test`
* sandboxtest - `make internal-sandbox-test` or `make prod-sandbox-test` depending on the environment

##### Running with poetry

In the root folder run the following command

```
PYTHONPATH=./tests poetry run pytest -v -m <TAG> <Path to file> --api-name=communications-manager --proxy-name=$PROXY_NAME --apigee-access-token=$APIGEE_ACCESS_TOKEN  --color=yes --junitxml=test-report.xml
```

- `PYTHONPATH=./tests` - Sets the root directory of the tests
- `poetry run pytest` - Runs pytest through poetry
- `-v` - Marks logs as verbose (Optional)
- `-m <TAG>` - Specifies tag name (Optional)
- `<relative path to file>` - Targets a specific file to run tests for, useful when developing new tests (Optional)
- `--api-name=communications-manager` - Specifies api name
- `--proxy-name=$PROXY_NAME` - Retrieves the PROXY_NAME environment variable and sets it to the proxy-name argument
- `--apigee-access-token=$APIGEE_ACCESS_TOKEN` - Retrieves the APIGEE_ACCESS_TOKEN environment variable and sets it to the apigee-access-token argument
- `--color=yes` - Displays logs in an easy to read format (Optional)
- `--junitxml=test-report.xml` - Sets the output of the test run, this will be located in the python path root directory for the tests

##### Troubleshooting

If your apigee access token does not refresh when generating a new token, try clearing cache before reattempting:

```export APIGEE_ACCESS_TOKEN=$(SSO_LOGIN_URL=https://login.apigee.com get_token --clear-sso-cache)```

#### Integration tests - long lived environments

There are several integration test suites configured within the `pytest.ini`, three of these are for testing our long lived environments - `int` and `prod`:

* inttest
* prodtest
* mtlstest

##### Python setup

Before running any tests you will need to build up your local environment to have access to the resources you need to successfully run tests, to do this run the `poetry install` command. This will populate the .venv directory. To source the .venv file, run source .venv/bin/activate in your shell type of choice:

* bash/zsh: `source .venv/bin/activate`
* csh: `source .venv/bin/activate.csh`
* fish: `source .venv/bin/activate.fish`
* nushell: `source .venv/bin/activate.nu`
* powershell: `. .venv/bin/activate.ps1`

##### Set up

For running tests against the integration and prod environments you must have created a client application within the [NHS onboarding portal](https://onboarding.prod.api.platform.nhs.uk/). The NHS onboarding portal allows you to create a client app that can be used to generate authorization bearer tokens to the API. This API uses [signed JWT authentication](https://digital.nhs.uk/developer/guides-and-documentation/security-and-authorisation/application-restricted-restful-apis-signed-jwt-authentication).

Once you have configured your client application you must then configure the following environmental variables:

* `INTEGRATION_API_KEY` - the API key for your integration environment application
* `INTEGRATION_PRIVATE_KEY` - the private key for your integration environment application
* `PRODUCTION_API_KEY` - the API key for your production environment application
* `PRODUCTION_PRIVATE_KEY` - the private key for your production environment application

Once these are set you can run the relevant integration (`inttest`) or production (`prodtest`) test suite.

##### Running with make

In the root folder run the following command:

* inttest - `make integration-test`
* prodtest - `make production-test`
* mtlstest - `make mtls-test`

##### Running with poetry

In the root folder run the following command

```
PYTHONPATH=./tests poetry run pytest -v -m <TAG> <Path to file> --color=yes --junitxml=test-report.xml
```

- `PYTHONPATH=./tests` - Sets the root directory of the tests
- `poetry run pytest` - Runs pytest through poetry
- `-v` - Marks logs as verbose (Optional)
- `-m <TAG>` - Specifies tag name (Optional)
- `<relative path to file>` - Targets a specific file to run tests for, useful when developing new tests (Optional)
- `--color=yes` - Displays logs in an easy to read format (Optional)
- `--junitxml=test-report.xml` - Sets the output of the test run, this will be located in the python path root directory for the tests

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

### Caveats

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

