#!/bin/bash

#run the docs generation
cd tests/docs/source && ./build-docs.sh && cd ../../../

#add the new docs
git add docs