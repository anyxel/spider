# Include shells
source ./core/scripts/libs/config.sh

tool_path="$et_dir/${tool_directory}"
zip_path="$et_dir/${tool_directory}.zip"

echo "Cleaning..."
# Check if the directory exists before attempting to delete it
if [ -d "$tool_path" ]; then
    echo "Deleting directory: $tool_path"
    try rm -r "$tool_path"
fi
if [ -e "$zip_path" ]; then
    echo "Deleting file: $zip_path"
    try rm "$zip_path"
fi


echo "Downloading $tool_directory..."
# try wget -O "$zip_path" "$git_repo/archive/$branch_name.zip"
try wget -nv --show-progress -O "$zip_path" "$git_repo/archive/$branch_name.zip"


echo "Extracting..."
try unzip -q -o $zip_path -d /app/et


echo "Renaming..."
try mv "${et_dir}/${tool_directory}-${branch_name}" "${tool_path}"


# Check if has_dependencies is true
if [ "$has_dependencies" = true ]; then
    echo "Installing dependencies..."
    try cd $tool_path && pip install -r requirements.txt
    echo "Dependencies installed."
fi


echo "Cleaning..."
try rm $zip_path

echo_green "Successfully installed!"
