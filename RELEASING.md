# Release process

We store our release candidate within the [release branch](https://github.com/NHSDigital/communications-manager-api) - this is the default branch for the repository.

## Create a release

To create a new release:

* Create a new release branch i.e. `release/v4.12.0`.
* Push a commit into the release branch that increments the version number - see release versioning commands.
* Create a PR from the release branch into `release`.
* Get approval on the PR and merge into `release`.
* Create a PR from `release` into `master`.
* Review the changes to be included in the release.
* Get approval on the PR and merge into `master`.
* The new release will be generated and uploaded to github.
* The release will run through the CI/CD pipeline, automatically deploying into `internal-dev`, `internal-dev-sandbox`, `internal-qa` and `internal-qa-sandbox`.
* The release will be held at this point, ready for deployment into our production environments.
* Ensure that the release has a change note uploaded to it, detailing the features/changes/fixes that went into the release.

## Promote a release to production environments

It is possible to self service promoting the release into the `sandbox`, `int` (integration) and `prod` environments. The process for this is:

* Access the [release CI/CD pipeline](https://dev.azure.com/NHSD-APIM/API%20Platform/_build?definitionId=620) for the specific release
* Approve the manual approval gates for `sandbox`, `int` or `prod` - to deploy the selected environment.

For `prod` to be released to both `sandbox` and `int` must have been released to successfully first.

## Release versioning commands

To increment the version number you need to add a command string into a commit message. The commit should include no changes other than the commit message.

The following commands can be used to control the version number:

* `+major`
* `+minor`
* `+patch`
* `+setstatus {status}`
* `+clearstatus`
* `+startversioning`

For the standard release process you will use either `+major`, `+minor` or `+patch`.

You can view the calculated version by running the `scripts/calculate_version.py` script:

```
$> python3 ./scripts/calculate_version.py
v3.2.0
```

### Examples

The following examples should provide commands that can be used in most situations.

#### Bump major version

To bump a major version - `1.2.3` to `2.0.0` - you can add an empty commit with the `+major` command in it:

```
$> git commit -m '+major' --allow-empty
$> git push origin release
```

#### Bump minor version

To bump a minor version - `1.2.3` to `1.3.0` - you can add an empty commit with the `+minor` command in it:

```
$> git commit -m '+minor' --allow-empty
$> git push origin release
```

#### Bump patch version

To bump a patch version - `1.2.3` to `1.2.4` - you can add an empty commit with the `+patch` command in it:

```
$> git commit -m '+patch' --allow-empty
$> git push origin release
```
