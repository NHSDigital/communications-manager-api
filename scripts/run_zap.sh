#!/bin/bash

set -o nounset
set -o errexit
set -o pipefail

# create our temporary directory
export TEMP_DIR=/tmp

echo "Storing reports in $TEMP_DIR"

# make sure we have published the spec
npm run publish

# we need to generate a zap compatible version of the spec
mv .python-version .python-version.ignore
python3 scripts/publish_zap_compatible.py
mv .python-version.ignore .python-version

# open the contents in INTEGRATION_PRIVATE_KEY and put it into INTEGRATION_PRIVATE_KEY_CONTENTS
export INTEGRATION_PRIVATE_KEY_CONTENTS=$(cat $INTEGRATION_PRIVATE_KEY)

docker build -t zap -f ./zap/Dockerfile .

# run zap in a container
docker container run \
    --env INTEGRATION_PRIVATE_KEY_CONTENTS="$INTEGRATION_PRIVATE_KEY_CONTENTS" \
    --env INTEGRATION_API_KEY="$INTEGRATION_API_KEY" \
    -v $(pwd):/zap/wrk/:rw \
    -v $TEMP_DIR:/zap/tmp/:rw \
    -v $(pwd)/zap/comms-manager-json/:/home/zap/.ZAP/reports/comms-manager-json/:rw \
    -t zap \
    bash -c "./zap.sh -addoninstallall -cmd -autorun /zap/wrk/zap/zap.yaml"

# generate our nunit report from the zap JSON report
./node_modules/.bin/hbs --data $TEMP_DIR/zap-report.json zap/nunit-template.hbs -s > zap-report.xml

# delete our zap compatible report
rm build/communications-manager-zap.json
