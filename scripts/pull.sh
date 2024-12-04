#!/bin/bash

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "Error: jq is not installed. Please install jq to use this script."
    exit 1
fi

# Virtool
repo_name="virtool"

url="https://api.github.com/repos/virtool/${repo_name}/releases/latest"

# Fetch the latest release tag name
tag_name=$(curl -s "$url" | jq -r '.tag_name')

# File to update
file_path="manifests/virtool/base/kustomization.yaml"

# Update the file with the fetched tag
if [[ -f "$file_path" ]]; then
    sed -i "s/newTag: [0-9.]\+/newTag: $tag_name/" "$file_path"
    echo "Updated $file_path with new tag: $tag_name"
else
    echo "Error: File $file_path not found."
    exit 1
fi

# UI
url="https://api.github.com/repos/virtool/virtool-ui/releases/latest"

# Fetch the latest release tag name
tag_name=$(curl -s "$url" | jq -r '.tag_name')

# File to update
file_path="manifests/ui/kustomization.yaml"

# Update the file with the fetched tag
if [[ -f "$file_path" ]]; then
    sed -i "s/newTag: [0-9.]\+/newTag: $tag_name/" "$file_path"
    echo "Updated $file_path with new tag: $tag_name"
else
    echo "Error: File $file_path not found."
    exit 1
fi

