#!/bin/bash

# Include shells
source ./tools/scripts/config.sh

# Variables
tool_path="$et_dir/Sublist3r"
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

echo "Downloading Sublist3r..."
wget -O $zip_path https://github.com/aboul3la/Sublist3r/archive/master.zip

echo "Extracting..."
unzip -o $zip_path -d /app/et
mv $et_dir/Sublist3r-master $tool_path

echo "Installing dependencies..."
cd $tool_path && pip install -r requirements.txt

echo "Cleaning..."
rm $zip_path

echo_green "Successfully installed!"
