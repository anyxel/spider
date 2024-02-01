#!/bin/bash

# Include shells
source ./core/scripts/libs/config.sh

echo "Installing nmap..."
try apt install nmap -y

echo_green "Successfully installed!"
