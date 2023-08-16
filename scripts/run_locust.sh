#!/bin/bash

poetry run locust -f tests/locust/test_no_errors.py --html tests/locust/no_errors.html --headless --host $HOST_URL || true;

sleep 60;

poetry run locust -f tests/locust/test_spike_arrest.py --html tests/locust/spike_arrest.html --headless --host $HOST_URL || true;

sleep 60;

poetry run locust -f tests/locust/test_quota.py --html tests/locust/quota.html --headless --host $HOST_URL || true;
