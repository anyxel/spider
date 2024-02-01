#!/bin/bash

# Include shells
source ./core/scripts/libs/config.sh

if command -v go &> /dev/null; then
    echo "Go is installed."
else
    echo "Installing Go..."

    try apt install golang-go -y
fi
