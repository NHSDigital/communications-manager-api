# Repoint Frontend

The "Repoint Frontend" script automates the process of reconfiguring the `communications-manager-api` APIs to point to a dynamic backend environment in the `comms-mgr` repository, rather than the default common backend in `internal-dev`.

## Overview

This script is especially useful when engineers are testing changes across both the `communications-manager-api` and `comms-mgr` repositories. By default, the `communications-manager-api` APIs point to a common backend in `internal-dev`, which is convenient when only `communications-manager-api` changes need testing. However, when changes span both `communications-manager-api` and `comms-mgr` and need testing in a specific dynamic environment (e.g., `de-todr3`), manual reconfiguration is required.

The script simplifies this process by automatically:

1. Pointing the APIs to the correct backend environment.
2. Disabling mTLS where necessary.

## Usage

```bash
./scripts/repoint-frontend/repoint_frontend.sh <ticket ID> <shortcode> [options]
```

e.g.
```bash
./scripts/repoint-frontend/repoint_frontend.sh 0000 todr3
```

Positional Arguments:

- `ticket ID`          Numeric ID of the ticket (e.g., '0000')
- `shortcode`          The environment identifier (e.g., 'todr3')

Options:

- `--help` Display usage information and exit, outlining all available commands
- `--list-steps` Display a list of each step the script will execute.
- `--from-step <n>` Begin execution from a specified step number.
- `--only-step <n>` Execute only a specified step.
