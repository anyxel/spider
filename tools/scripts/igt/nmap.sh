#!/bin/bash

# Include shells
source ./core/scripts/libs/config.sh

if command -v nmap &> /dev/null
then
    echo_yellow "Nmap is already installed!"
else
    echo "Installing Nmap..."
    try apt install nmap -y
    echo_green "Successfully installed!"
fi
