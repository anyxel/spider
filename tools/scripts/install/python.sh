# Include shells
source ./tools/scripts/config.sh

tool_path="$et_dir/${tool_directory}"
zip_path="$et_dir/${tool_directory}.zip"

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


echo "Downloading $tool_directory..."
wget -O "$zip_path" "$git_repo/archive/$branch_name.zip"


echo "Extracting..."
unzip -o $zip_path -d /app/et


echo "Renaming..."
mv "${et_dir}/${tool_directory}-${branch_name}" "${tool_path}"


# Check if has_dependencies is true
if [ "$has_dependencies" = true ]; then
    echo "Installing dependencies..."
    cd $tool_path && pip install -r requirements.txt
    echo "Dependencies installed."
fi


echo "Cleaning..."
rm $zip_path

echo_green "Successfully installed!"
