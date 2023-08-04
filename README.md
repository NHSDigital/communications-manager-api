# communications-manager

## Status

* Nightly test status: [![Nightly test status](https://dev.azure.com/NHSD-APIM/API%20Platform/_apis/build/status%2FCommunications-Manager%2FCommunications-Manager-Nightly?repoName=NHSDigital%2Fcommunications-manager&branchName=master)](https://dev.azure.com/NHSD-APIM/API%20Platform/_build/latest?definitionId=622&repoName=NHSDigital%2Fcommunications-manager&branchName=master)

This is a specification for the *communications-manager* API.

* `specification/` This [Open API Specification](https://swagger.io/docs/specification/about/) describes the endpoints, methods and messages exchanged by the API. Use it to generate interactive documentation; the contract between the API and its consumers.
* `sandbox/` This NodeJS application implements a mock implementation of the service. Use it as a back-end service to the interactive documentation to illustrate interactions and concepts. It is not intended to provide an exhaustive/faithful environment suitable for full development and testing.
* `scripts/` Utilities helpful to developers of this specification.
* `proxies/` Live (connecting to another service) and sandbox (using the sandbox container) Apigee API Proxy definitions.

Consumers of the API will find developer documentation on the [NHS Digital Developer Hub](https://digital.nhs.uk/developer).

## Contributing
Contributions to this project are welcome from anyone, providing that they conform to the [guidelines for contribution](https://github.com/NHSDigital/communications-manager/blob/master/CONTRIBUTING.md) and the [community code of conduct](https://github.com/NHSDigital/communications-manager/blob/master/CODE_OF_CONDUCT.md).

### Licensing
This code is dual licensed under the MIT license and the OGL (Open Government License). Any new work added to this repository must conform to the conditions of these licenses. In particular this means that this project may not depend on GPL-licensed or AGPL-licensed libraries, as these would violate the terms of those libraries' licenses.

The contents of this repository are protected by Crown Copyright (C).

## Releasing

Our release process is [documented here](https://github.com/NHSDigital/communications-manager/blob/release/RELEASING.md).

## Development

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
You can install some pre-commit hooks to ensure you can't commit invalid spec changes by accident. These are also run
in CI, but it's useful to run them locally too.

```
$ make install-hooks
```

### Environment Variables
Various scripts and commands rely on environment variables being set. These are documented with the commands.

:bulb: Consider using [direnv](https://direnv.net/) to manage your environment variables during development and maintaining your own `.envrc` file - the values of these variables will be specific to you and/or sensitive.

### Make commands
There are `make` commands that alias some of this functionality:
 * `lint` -- Lints the spec and code
 * `publish` -- Outputs the specification as a **single file** into the `build/` directory
 * `serve` -- Serves a preview of the specification in human-readable format

### Testing
Each API and team is unique. We encourage you to use a `test/` folder in the root of the project, and use whatever testing frameworks or apps your team feels comfortable with. It is important that the URL your test points to be configurable. We have included some stubs in the Makefile for running tests.

##### Set up
Before running your tests you need to generate an [apigee access token](https://nhsd-confluence.digital.nhs.uk/display/APM/Test+Utils+2.0%3A+Running+tests). To generate a token run the following command, you will then be prompted to log in to apigee with your username, password and MFA code.

```
export APIGEE_ACCESS_TOKEN=$(SSO_LOGIN_URL=https://login.apigee.com get_token)
```

Set the `PROXY_NAME` environment variable to the environment you want to run the tests on. You can find the proxy name by logging into [Apigee](https://apigee.com/edge), navigating to 'API Proxies' and searching for 'communications-manager', this will show you a list of available proxies, eg:
- communications-manager-internal-dev
- communications-manager-internal-dev-sandbox
- communications-manager-pr-{num}
- communications-manager-pr-{num}-sandbox

Before running any tests you will need to build up your local environment to have access to the resources you need to successfully run tests, to do this run the `poetry install` command. This will populate the .venv directory. To source the .venv file, run source .venv/bin/activate in your shell type of choice

- bash/zsh: `source .venv/bin/activate`
- csh: `source .venv/bin/activate.csh`
- fish: `source .venv/bin/activate.fish`
- nushell: `source .venv/bin/activate.nu`
- powershell: `. .venv/bin/activate.ps1`

##### Run tests through make command
In the root folder run the following command:

Run a subset of tests marked 'devtest'

`make dev-test`

Run a subset of tests marked 'smoketest'

`make smoketest`

Run a subset of tests marked 'sandboxtest'

`make sandboxtest`

##### Running tests through command line 
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

##### Troubleshooting:
If your apigee access token does not refresh when generating a new token, try clearing cache before reattempting

```export APIGEE_ACCESS_TOKEN=$(SSO_LOGIN_URL=https://login.apigee.com get_token --clear-sso-cache)```

```export APIGEE_ACCESS_TOKEN=$(SSO_LOGIN_URL=https://login.apigee.com get_token)```

### VS Code Plugins

 * [openapi-lint](https://marketplace.visualstudio.com/items?itemName=mermade.openapi-lint) resolves links and validates entire spec with the 'OpenAPI Resolve and Validate' command
 * [OpenAPI (Swagger) Editor](https://marketplace.visualstudio.com/items?itemName=42Crunch.vscode-openapi) provides sidebar navigation


### Emacs Plugins

 * [**openapi-yaml-mode**](https://github.com/esc-emacs/openapi-yaml-mode) provides syntax highlighting, completion, and path help

### Speccy

> [Speccy](http://speccy.io/) *A handy toolkit for OpenAPI, with a linter to enforce quality rules, documentation rendering, and resolution.*

Speccy does the lifting for the following npm scripts:

 * `test` -- Lints the definition
 * `publish` -- Outputs the specification as a **single file** into the `build/` directory
 * `serve` -- Serves a preview of the specification in human-readable format

(Workflow detailed in a [post](https://developerjack.com/blog/2018/maintaining-large-design-first-api-specs/) on the *developerjack* blog.)

:bulb: The `publish` command is useful when uploading to Apigee which requires the spec as a single file.

### Caveats

#### Swagger UI
Swagger UI unfortunately doesn't correctly render `$ref`s in examples, so use `speccy serve` instead.

#### Apigee Portal
The Apigee portal will not automatically pull examples from schemas, you must specify them manually.

### Platform setup

As currently defined in your `proxies` folder, your proxies do pretty much nothing.
Telling Apigee how to connect to your backend requires a *Target Server*, which you should call named `communications-manager-target`.
Our *Target Servers* defined in the [api-management-infrastructure](https://github.com/NHSDigital/api-management-infrastructure) repository.

:bulb: For Sandbox-running environments (`test`) these need to be present for successful deployment but can be set to empty/dummy values.

### Detailed folder walk through
To get started developing your API use this template repo alongside guidance provided by the [API Producer Zone confluence](https://nhsd-confluence.digital.nhs.uk/display/APM/Deliver+your+API)

#### `/.github`:

This folder contains templates that can be customised for items such as opening pull requests or issues within the repo

`/.github/workflows`: This folder contains templates for github action workflows such as:
- `pr-lint.yaml`: This workflow template shows how to link Pull Request's to Jira tickets and runs when a pull request is opened.
- `continuous-integration.yml`: This workflow template shows how to publish a Github release when pushing to master.

#### `/azure`:

Contains templates defining Azure Devops pipelines. By default the following pipelines are available:
-  `azure-build-pipeline.yml`: Assembles the contents of your repository into a single file ("artifact") on Azure Devops and pushes any containers to our Docker registry. By default this pipeline is enabled for all branches.
- `azure-pr-pipeline.yml`: Deploys ephemeral versions of your proxy/spec to Apigee (and docker containers on AWS) to internal environments. You can run automated and manual tests against these while you develop. By default this pipeline will deploy to internal-dev, but the template can be amended to add other environments as required.
- `azure-release-pipeline.yml`: Deploys the long-lived version of your pipeline to internal and external environments, typically when you merge to master.

The `project.yml` file needs to be populated with your service names to make them available to the pipelines

`/azure/templates`: Here you can define reusable actions, such as running tests, and call these actions during Azure Devops pipelines. 

#### `/proxies`:

This folder contains files relating to your Apigee API proxy.

There are 2 folders `/live` and `/sandbox` allowing you to define a different proxy for sandbox use. By default, this sandbox proxy is implemented to route to the sandbox target server (code for this sandbox is found under /sandbox of this template repo)

Within the `live/apiproxy` and `sandbox/apiproxy` folders are:

`/proxies/default.xml`: Defines the proxy's Flows. Flows define how the proxy should handle different requests. By default, _ping and _status endpoint flows are defined.
See the APM confluence for more information on how the [_ping](https://nhsd-confluence.digital.nhs.uk/display/APM/_ping+endpoint) and [_status](https://nhsd-confluence.digital.nhs.uk/display/APM/_status+endpoint) endpoints work.

`/policies`: Populated with a set of standard XML Apigee policies that can be used in flows.

`/resources/jsc`: Snippets of javascript code that are used in Apigee Javascript policies. For more info about Javascript policies see [here](https://docs.apigee.com/api-platform/reference/policies/javascript-policy)

`/targets`: The XMLs within these folders set up target definitions which allow connections to external target servers. The sandbox target definition is implemented to route to the sandbox target server (code for this sandbox is found under /sandbox of this template repo). For more info on setting up a target server see the [API Producer Zone confluence](https://nhsd-confluence.digital.nhs.uk/display/APM/Setting+up+a+target+server)

#### `/sandbox`:

This folder contains a template for a sandbox API. This example is a NodeJs application running in Docker. The application handles a few simple endpoints such as: /_ping, /health, /_status, /hello and some logging logic.
For more information about building sandbox APIs see the [API Producer Zone confluence](https://nhsd-confluence.digital.nhs.uk/display/APM/Setting+up+your+API+sandbox ).

#### `/scripts`:

Contains useful scripts that are used throughout the project, for example in Makefile and Github workflows

#### `/specification`:

Create an OpenAPI Specification to document your API. For more information about developing specifications see the [API Producer Zone confluence](https://nhsd-confluence.digital.nhs.uk/display/APM/Documenting+your+API).

#### `/tests`:

End to End tests. These tests are written in Python and use the PyTest test runner. Before running these tests you will need to set environment variables. The `test_endpoint.py` file provides a template of how to set up tests which test your api endpoints. For more information about testing your API see the [API Producer Zone confluence](https://nhsd-confluence.digital.nhs.uk/display/APM/Testing+your+API ).

#### `Makefile`:
Useful make targets to get started including: installing dependencies and running smoke tests.

#### `ecs-proxies-containers.yml ` and `ecs-proxies-deploy.yml`:

These files are required to deploy containers alongside your Apigee proxy during the Azure Devops `azure-build-pipeline`. In this template repo we are deploying our sandbox container which is used as the target server for the sandbox proxy.

`ecs-proxies-containers.yml`: The path to a container's Dockerfile is defined here. This path needs to be defined to allow containers to be pushed to our repository during the `azure-build-pipeline`.

`ecs-proxies-deploy.yml` : Here you can define config for your container deployment.  

For more information about deploying ECS containers see the [API Producer Zone confluence](https://nhsd-confluence.digital.nhs.uk/display/APM/Developing+ECS+proxies#DevelopingECSproxies-Buildingandpushingdockercontainers ).

#### `manifest_template.yml`:

This file defines 2 dictionaries of fields that are required for the Apigee deployment. For more info see the [API Producer Zone confluence](https://nhsd-confluence.digital.nhs.uk/display/APM/Manifest.yml+reference ).

#### Package management:

This template uses poetry for python dependency management, and uses these files: poetry.lock, poetry.toml, pyproject.toml.

Node dependencies of this template project and some npm scripts are listed in: package.json, package-lock.json.

#### Postman:
Included in this repo is a postman collection that allows the user to interact with the API directly. 

To use the collection:
- Download the json files located in the postman directory
- Import the files into postman
- Select a target environment in postman
- Set the environment variables 'api-key' and 'private-key' for the desired environment (this does not apply for sandbox)
- Run the collection

The collection is ordered so that the first request ran when running a collection is 'Generate token', this generates an authorization header that is re-used for subsequent requests in the collection. The authorization header expires after 10 minutes, so if you are using this collection to manually execute requests and get an unexpected '401' execute the 'Generate token' request again to refresh your token.
