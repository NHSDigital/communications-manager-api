#!/bin/bash

poetry run locust -f tests/locust/tests/stress_test.py --html tests/locust/results/stress_test.html --headless --host $HOST_URL || true;