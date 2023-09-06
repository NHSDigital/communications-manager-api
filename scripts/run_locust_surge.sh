#!/bin/bash

poetry run locust -f tests/locust/tests/surge_test.py --html tests/locust/results/surge_test.html --headless --host $HOST_URL || true;