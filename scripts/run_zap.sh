#!/bin/bash

set -o nounset errexit pipefail

# create our temporary directory
export TEMP_DIR=/tmp

echo "Storing reports in $TEMP_DIR"

# make sure we have published the spec
npm run publish

# run zap in a container
docker container run \
    -v $(pwd):/zap/wrk/:rw \
    -v $TEMP_DIR:/zap/tmp/:rw \
    -v $(pwd)/zap/comms-manager-json/:/home/zap/.ZAP/reports/comms-manager-json/:rw \
    -t softwaresecurityproject/zap-stable bash \
    -c "./zap.sh -addoninstall openapi -cmd -autorun /zap/wrk/zap/zap.yaml"

# generate our nunit report from the zap JSON report
./node_modules/.bin/hbs --data $TEMP_DIR/zap-report.json zap/nunit-template.hbs -s > zap-report.xml
