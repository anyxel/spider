#!/bin/bash

if command -v go &> /dev/null; then
    echo "Go is installed."
else
    echo "Installing golang..."
    apt install golang-go -y
fi
