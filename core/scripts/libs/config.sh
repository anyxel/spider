#!/bin/bash

# Include shells
source ./core/scripts/libs/color.sh

# Variables
et_dir="/app/et"

# Try catch
try() {
    "$@" || { echo_red "Error occurred during: $*"; exit 1; }
}
