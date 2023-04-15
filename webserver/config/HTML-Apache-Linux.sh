#!/bin/bash

# [ NOTE ] This does NOT cover telling Apache to hide config from users!!

# Check if root
if [ "$EUID" -ne 0 ]
    then echo "Please run this as root to copy to web directory!"
    exit
fi

# Get the name of the software from the first argument
SOFTWARE_NAME=$1

# If the software name is not set, exit
if [ -z "$SOFTWARE_NAME" ]; then
    echo "Please provide the name of the software as the first argument!"
    exit
fi

# Get the current directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# If the /var/www/html/SOFTWARE_NAME directory already exists, delete it
if [ -d "/var/www/html/$SOFTWARE_NAME" ]; then
    rm -rf /var/www/html/$SOFTWARE_NAME
fi

# Create the /var/www/html/SOFTWARE_NAME directory
mkdir /var/www/html/$SOFTWARE_NAME

# Copy the HTML directory to the web root at /var/www/html/SOFTWARE_NAME
cp -r "$DIR/../." "/var/www/html/$SOFTWARE_NAME"

# Change the ownership of the directory to apache
chown -R apache:apache /var/www/html/$SOFTWARE_NAME

# Restart Apache
systemctl restart httpd

# Tell "success" to user
echo "Apache has been restarted and the HTML directory has been copied to /var/www/html/$SOFTWARE_NAME"