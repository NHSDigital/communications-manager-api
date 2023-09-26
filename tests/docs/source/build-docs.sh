#!/bin/bash

export PYTHONPATH=../../

#clean
rm -rf ../build

#run the build
sphinx-build -M markdown ./ ../build

#clear the doctrees
rm -rf ../build/doctrees

#remove all headers that match the regex
for f in $(find ../build/markdown -name '*.md') ; do
    TARGET_PATH=${f//..\/build\/markdown\//} ;
    mkdir -p ../build/${TARGET_PATH//$(basename $f)} ;
    grep -v -E '### \w+\..*?\)' $f > ../build/$TARGET_PATH ;
done

#remove the original markdown folder
rm -rf ../build/markdown

#move the build to the docs location
rm -rf ../../../docs/tests/
mv ../build ../../../docs/tests