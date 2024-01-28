#!/bin/bash

# Include shells
source ./tools/scripts/config.sh

echo "Installing nmap..."
apt install nmap -y

echo_green "Successfully installed!"
