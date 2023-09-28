#!/bin/bash

set -euo pipefail

source ../../.venv/bin/activate

if [ "$1" == "--verify" ]; then
    OLD_VERIFICATION_HASH=$(find ../../docs/tests -name "*.md" -type f -exec md5sum {} \; | md5sum)
    OLD_VERIFICATION_HASH=${OLD_VERIFICATION_HASH// -}
    echo "Verifying documentation is up to date, existing documentation hash is $OLD_VERIFICATION_HASH"
fi

export PYTHONPATH=../

#clean
rm -rf build

#run the build
sphinx-build -M markdown . build

#clear the doctrees
rm -rf build/doctrees

#remove all headers that match the regex
for f in $(find build/markdown -name '*.md') ; do
    TARGET_PATH=${f//build\/markdown\//} ;
    mkdir -p build/${TARGET_PATH//$(basename $f)} ;
    grep -v -E '### \w+\..*?\)' $f > build/$TARGET_PATH ;
done

#remove the original markdown folder
rm -rf build/markdown

#move the build to the docs location
rm -rf ../../docs/tests/
mv build ../../docs/tests

if [ "$1" == "--verify" ]; then
    NEW_VERIFICATION_HASH=$(find ../../docs/tests -name "*.md" -type f -exec md5sum {} \; | md5sum)
    NEW_VERIFICATION_HASH=${NEW_VERIFICATION_HASH// -}
    echo "After documentation build hash is $NEW_VERIFICATION_HASH"

    if [ "$OLD_VERIFICATION_HASH" != "$NEW_VERIFICATION_HASH" ]; then
        echo "!!!!!! Documentation hash mismatch, erroring"
        exit 1
    fi
fi