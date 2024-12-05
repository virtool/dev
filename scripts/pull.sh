#!/bin/bash

# Ensure jq is installed
if ! command -v jq &> /dev/null; then
    echo "Error: jq is not installed. Please install jq to use this script."
    exit 1
fi

fetch_and_update() {
    local repo=$1
    local file=$2
    local prefix=$3

    # Fetch the latest release tag
    local url="https://api.github.com/repos/${repo}/releases/latest"
    local tag=$(curl -s "$url" | jq -r '.tag_name')

    # Update the file if it exists
    if [[ -f "$file" ]]; then
        sed -i "s/${prefix}[0-9.]\+/${prefix}${tag}/" "$file"
        echo "Using tag '$tag' for $file"
    else
        echo "Error: File $file not found."
        exit 1
    fi
}

echo "Server"
echo ""

fetch_and_update "virtool/virtool" "manifests/virtool/base/kustomization.yaml" "newTag: "
fetch_and_update "virtool/virtool-ui" "manifests/ui/kustomization.yaml" "newTag: "

echo ""
echo "Workflows"
echo ""

for workflow in "build-index" "create-sample" "create-subtraction" "iimi" "nuvs" "pathoscope"; do
    fetch_and_update "virtool/workflow-${workflow}" "manifests/workflows/${workflow}.yaml" "${workflow}:"
done