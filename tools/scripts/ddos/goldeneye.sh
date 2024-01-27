#!/bin/bash

# Include shells
source ./tools/scripts/config.sh

# Variables
tool_path="$et_dir/GoldenEye"
zip_path="$et_dir/sublist3r.zip"

echo "Cleaning..."
# Check if the directory exists before attempting to delete it
if [ -d "$tool_path" ]; then
    echo "Deleting directory: $tool_path"
    rm -r "$tool_path"
fi
if [ -e "$zip_path" ]; then
    echo "Deleting file: $zip_path"
    rm "$zip_path"
fi

echo "Downloading GoldenEye..."
wget -O $zip_path https://github.com/jseidl/GoldenEye/archive/master.zip

echo "Extracting..."
unzip -o $zip_path -d /app/et
mv $et_dir/GoldenEye-master $tool_path

echo "Cleaning..."
rm $zip_path

echo_green "Successfully installed!"
