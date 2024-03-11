#!/bin/bash

# Include shells
source ./core/scripts/install/languages/go.sh

echo "Installing Dalfox..."
try go install github.com/hahwul/dalfox/v2@latest

echo_green "Successfully installed!"
