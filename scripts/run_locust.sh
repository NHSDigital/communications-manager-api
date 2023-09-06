#!/bin/bash

poetry run locust -f tests/locust/tests/test_no_errors.py --html tests/locust/results/no_errors.html --headless --host $HOST_URL || true;

echo "Sleeping for 60 seconds"

sleep 60;

poetry run locust -f tests/locust/tests/test_spike_arrest.py --html tests/locust/results/spike_arrest.html --headless --host $HOST_URL || true;

echo "Sleeping for 60 seconds"

sleep 60;

poetry run locust -f tests/locust/tests/test_quota.py --html tests/locust/results/quota.html --headless --host $HOST_URL || true;

#echo $PYTHONPATH
