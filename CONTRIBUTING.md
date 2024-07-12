# Contribution Guidelines

## Raising an Issue
If you raise an issue against this repository, please include as much information as possible to reproduce any bugs,
or specific locations in the case of content errors.

## Contributing code
To contribute code, please fork the repository and raise a pull request.

Ideally pull requests should be fairly granular and aim to solve one problem each. It would also be helpful if they
linked to an issue. If the maintainers cannot understand why a pull request was raised, it will be rejected,
so please explain why the changes need to be made (unless it is self-evident).

### Merge responsibility
* It is the responsibility of the reviewer to merge branches they have approved.
* It is the responsibility of the author of the merge to ensure their merge is in a mergeable state.
* It is the responsibility of the maintainers to ensure the merge process is unambiguous and automated where possible.

### Branches

All changes are created on a short lived branch specifically for that change. Once ready, the branch must be merged into the `release` branch via a Pull Request.

Branch names must follow the format below:

```
feature/${jira-ticket-number}_${precis-of-branch-purpose}
```

e.g.

```
feature/CCM-1234_cicd-documentation
```

Other branch prefixes that can be used are `chore`, and `fix`.

The only merge strategy via Github is `Squash and merge`. If the merging is performed locally, every effort should be made to ensure only one commit is merged into the `release` branch. This is to keep a clean, concise history.

### Commit messages
Commit messages should be formatted as follows:
```
CCM-1234: Summary of changes

Longer description of changes if explaining rationale is necessary,
limited to 80 columns and spanning as many lines as you need.
```

