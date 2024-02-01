#!/bin/bash

# Include shells
source ./core/scripts/libs/config.sh

if command -v go &> /dev/null; then
    echo_yellow "Go version: $(go version)"
else
    echo "Installing Go..."

    try apt install golang-go -y
fi
