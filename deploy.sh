#!/bin/bash
set -e

echo "removing build directory"
echo "rm -rf build"
rm -rf build

echo ""
echo "building pygbag web executable"
echo "pygbag --build --icon favicon.ico ."
pygbag --build --icon favicon.ico .
