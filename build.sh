#!/bin/bash
mkdir -p build
cp app.py build/
cp -r templates build/
cd build
sha256sum app.py > hash.txt
