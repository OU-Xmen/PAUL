#!/bin/bash

# Get the absolute path of the current directory
DIRECTORY_NAME=$(realpath "$(dirname "$0")")
# Move up two directories
DIRECTORY_NAME=$(realpath "$DIRECTORY_NAME/../..")

# Define the directory to search for HTML files (DIRECTORY_NAME plus /docs)
search_dir="$DIRECTORY_NAME/docs"

# Define the name of the output HTML file (DIRECTORY_NAME plus /docs/index.html)
output_file="$DIRECTORY_NAME/docs/index.html"

# Remove output_file if it exists
if [ -f "$output_file" ]; then
    rm "$output_file"
fi

# Generate the list of HTML files
html_files=$(find $search_dir -name "*.html")

# Remove all duplicates from the list of HTML files
html_files=$(echo "$html_files" | sort | uniq)

# Generate the content for the HTML file, including bootstrap
html_content+="<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>Pydoctor-Plus API Docs</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-KK94CHFLLe+nY2dmCWGMq91rCGa5gtU4mk92HdvYe+M/SXH301p5ILy+dN9+nJOZ" crossorigin="anonymous">
</head>
<body>
    <div class='container'>
    <h1 class='text-center'>Welcome to Pydoctor-Plus API Docs</h1>
    <p class='text-center'>Click on a link below to view the documentation for a specific module.</p>
    <ul class='list-group'>"

# Set IFS=$'\n'
IFS=$'\n'

# Loop through each HTML file and add a link to the HTML content
for file_path in $html_files
do
    file_name=$(basename "$file_path")
    temp_path=$(realpath --relative-to="$search_dir" "$file_path")
    temp_path=$(dirname "$temp_path")
    relative_path=$(realpath --relative-to="$search_dir" "$file_path")
    # If the file name is index.html, then set the relative path to the parent directory
    if [ "$file_name" = "index.html" ]; then
        # Add the link to the HTML content
        html_content+="      <li class='list-group-item'><a href='$relative_path'>$temp_path</a></li>"
        echo "Preparing HTML content: $file_name\r"
    fi
done

# Finish generating the HTML content
html_content+="    </ul>
    </div>
    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ENjdO4Dr2bkBIFxQpeoTz1HIcje39Wm4jDKdf19U8gI4ddQ3GYNS7NTKfAdVQSZe" crossorigin="anonymous"></script>
</body>
</html>"

# Write the HTML content to the output file
echo $html_content > $output_file

# Echo success to user
echo "Successfully generated $output_file!"