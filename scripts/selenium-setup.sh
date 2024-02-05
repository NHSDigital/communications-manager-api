#!/bin/bash

cd tests/selenium/drivers

CHROME_LATEST_VERSION_DOWNLOADS=$(curl https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json)
CHROME_URL=$(echo $CHROME_LATEST_VERSION_DOWNLOADS | jq -r '.channels.Stable.downloads.chrome [].url' | grep linux64)
CHROMEDRIVER_URL=$(echo $CHROME_LATEST_VERSION_DOWNLOADS | jq -r '.channels.Stable.downloads.chromedriver [].url' | grep linux64)

wget $CHROME_URL

wget $CHROMEDRIVER_URL

unzip chrome-linux64.zip
unzip chromedriver-linux64.zip

rm -rf drivers/*.zip