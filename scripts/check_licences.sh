#!/bin/sh
npm run check-licenses && scripts/check_python_licenses.sh && cd sandbox && npm run check-licenses