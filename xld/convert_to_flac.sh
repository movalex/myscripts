#!/bin/bash

# Function to display usage instructions
usage() {
    echo "Usage: $0 [path_element]"
    echo "path_element: Optional. If provided, it is appended to the cue filename pattern like '*path_element.cue'."
    exit 1
}

# Check if xld command exists
if ! command -v xld &> /dev/null
then
    echo "xld command could not be found. Please make sure it is installed."
    exit 1
fi

# Parse the optional path element argument
path_element=""

if [[ $# -eq 1 ]]; then
    path_element="$1"
elif [[ $# -gt 1 ]]; then
    usage
fi

# How many directories we have to process
dir_count=$(find . -maxdepth 1 -type d | wc -l)
progress_file=$(mktemp)
echo 0 > "$progress_file"

# Function to display progress
display_progress() {
    local progress=$(cat "$progress_file")
    echo -ne "Processing directories: $progress/$((dir_count - 1))\r"
}

# Function to process a directory
process_directory() {
    dir="$1"

    # Enter the directory
    cd "$dir" || { echo "Failed to enter directory $dir"; exit 1; }

    # Find the .cue files with the path element
    cue_files=(*"${path_element}.cue")

    if [[ -e "${cue_files[0]}" ]]; then
        # Run xld command to create FLAC files
        xld -c *"${path_element}.cue" -f flac *.flac >/dev/null 2>&1
    fi

    # Return to the parent directory
    cd ..

    # Update progress
    {
        flock -x 200
        local progress=$(($(cat "$progress_file") + 1))
        echo "$progress" > "$progress_file"
    } 200>"$progress_file.lock"

    # Refresh display
    display_progress
}

# Loop through each directory in the current directory and process concurrently
for dir in */; do
    process_directory "$dir" &
done

# Wait for all background processes to complete
wait

# Clean up
rm "$progress_file" "$progress_file.lock"

echo -e "\nDone processing all directories."
