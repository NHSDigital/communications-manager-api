#!/bin/bash

set -o nounset errexit pipefail

# Collect the API Proxy and Hosted Target (Sandbox server)
# files into build/apiproxy/ and deploy to Apigee

rm -rf build/proxies
mkdir -p build/proxies/sandbox
mkdir -p build/proxies/live
cp -Rv proxies/sandbox/apiproxy build/proxies/sandbox
cp -Rv proxies/live/apiproxy build/proxies/live

# copy over our shared policies
cp -Rv proxies/shared/* build/proxies/sandbox/apiproxy/
cp -Rv proxies/shared/* build/proxies/live/apiproxy/

source .venv/bin/activate

# generate our final XML with some includes
python3 scripts/process_imports.py build/proxies/sandbox/apiproxy/
python3 scripts/process_imports.py build/proxies/live/apiproxy/

# clear our partials
rm -rf build/proxies/sandbox/apiproxy/partials
rm -rf build/proxies/live/apiproxy/partials