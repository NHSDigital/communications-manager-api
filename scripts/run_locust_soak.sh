#!/bin/bash

poetry run locust -f tests/locust/tests/soak_test.py --html tests/locust/results/soak_test.html --headless --host $HOST_URL || true;