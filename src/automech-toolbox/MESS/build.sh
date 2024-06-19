#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
PREFIX=${SCRIPT_DIR}/static

(
    cd ${SCRIPT_DIR}
    mkdir -p build
    cd build
    
    cmake .. -DCMAKE_INSTALL_PREFIX=${PREFIX}
    
    make VERBOSE=1
)

