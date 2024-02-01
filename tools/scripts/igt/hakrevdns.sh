#!/bin/bash

# Include shells
source ./core/scripts/install/languages/go.sh

echo "Installing Hakrevdns..."
try go install github.com/hakluke/hakrevdns@latest

echo_green "Successfully installed!"
