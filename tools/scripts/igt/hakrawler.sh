#!/bin/bash

# Include shells
source ./core/scripts/install/languages/go.sh

echo "Installing Hakrawler..."
try go install github.com/hakluke/hakrawler@latest

echo_green "Successfully installed!"
