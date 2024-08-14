#!/bin/bash
find . -name "*.py" -not -path "**/.venv/*" | xargs poetry run flake8
