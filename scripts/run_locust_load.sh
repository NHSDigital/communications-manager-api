#!/bin/bash

poetry run locust -f tests/locust/tests/load_test.py --html tests/locust/results/load_test.html --headless --host $HOST_URL || true;