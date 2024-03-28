#!/bin/bash

# Include shells
source ./core/scripts/install/languages/go.sh

echo "Installing GoSpider..."
try go install github.com/jaeles-project/gospider@latest

echo_green "Successfully GoSpider!"
