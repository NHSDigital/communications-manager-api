#!/bin/bash

poetry run locust -f tests/locust/tests/capacity_test.py --html tests/locust/results/capacity_test.html --headless --host $HOST_URL || true;