#!/bin/bash

# Check if xld command exists
if ! command -v xld &> /dev/null
then
    echo "xld command could not be found. Please make sure it is installed."
    exit 1
fi

# Function to process a directory
process_directory() {
    dir="$1"
    path="$2"

    # Check if there are any .cue files in the directory
    if compgen -G "$dir/*$path.cue" > /dev/null; then
        echo "Processing directory: $dir"
        echo "Option: $path"

        # Enter the directory
        cd "$dir" || { echo "Failed to enter directory $dir"; exit 1; }

        # Run xld command to create FLAC files
        xld -c "*$path.cue" -f flac *.flac

        # Return to the parent directory
        cd ..
    else
        echo "No .cue files found in directory: $dir, skipping..."
    fi
}

# Loop through each directory in the current directory and process concurrently
for dir in */; do
    process_directory "$dir" &
done

# Wait for all background processes to complete
wait

echo "Done processing all directories."
