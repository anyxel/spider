#!/bin/bash

# ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print in green
echo_green() {
    echo -e "${GREEN}$1${NC}"
}

# Function to print in red
echo_red() {
    echo -e "${RED}$1${NC}"
}

# Function to print in yellow
echo_yellow() {
    echo -e "${YELLOW}$1${NC}"
}
