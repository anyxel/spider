#!/bin/bash

installation_script="./core/scripts/install/tools/${tool_language}.sh"

if [ -f "$installation_script" ]; then
    source "$installation_script"
else
    echo "No installation file found for the specified language: $tool_language."
fi
