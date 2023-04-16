#!/bin/bash

# Get the absolute path of the current directory
DIRECTORY_NAME=$(realpath "$1")

# Print the directory name
echo "Attempting to generate documentation for $DIRECTORY_NAME"

# Set full docs directory path from $DIRECTORY_NAME plus /docs
DOCS_DIRECTORY=$DIRECTORY_NAME/docs

# Set IFS=$'\n'
IFS=$'\n'

# Loop through each python file in $DIRECTORY_NAME
for FILE in $(find "$DIRECTORY_NAME" -type f -name '*.py'); do
    # Get the relative path of FILE from $DIRECTORY_NAME
    RELATIVE_PATH=$(realpath --relative-to="$DIRECTORY_NAME" "$FILE")
    
    # Generate the documentation for the current file
    echo "Working on $FILE"
    python3 -m pydoctor --make-html --html-output="$DOCS_DIRECTORY/$RELATIVE_PATH" "$FILE"
done

# Tell "success" to user
echo "Successfully generated documentation!"