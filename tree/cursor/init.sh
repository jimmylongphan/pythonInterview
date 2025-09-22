#!/bin/bash

# Define the repository URL
REPO_URL="https://github.com/postgres/postgres.git"

# Define the directory where the repository will be cloned
CLONE_DIR="postgres"

# Clone only the top level of the repository
git clone --depth 1 $REPO_URL $CLONE_DIR

# Check if the clone was successful
if [ $? -eq 0 ]; then
    echo "Repository cloned successfully into $CLONE_DIR"
else
    echo "Failed to clone the repository"
    exit 1
fi

