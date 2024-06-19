#!/usr/bin/env bash

set -e  # if any command fails, quit
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
PREFIX=${SCRIPT_DIR}/static

# 1. Build the executables using CMake
(
    mkdir -p build
    cd build
    
    cmake ${SCRIPT_DIR} -DCMAKE_INSTALL_PREFIX=${PREFIX}
    
    make VERBOSE=1
    make install
)

# 2. Create the conda package using rattler-build
rattler-build build -r ${SCRIPT_DIR}/.recipe/
echo "You can upload your packages with the following command:"
echo "  rattler-build upload anaconda -o Auto-Mech output/noarch/*.conda"
echo "which will upload the following artifacts to Anaconda.org:"
ls -la output/noarch/*.conda
