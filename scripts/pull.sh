#!/bin/bash

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "Error: jq is not installed. Please install jq to use this script."
    exit 1
fi

echo "Server"

update_tag() {
    local repo_name=$1
    local file_path=$2

    # Fetch the latest release tag name
    local url="https://api.github.com/repos/virtool/${repo_name}/releases/latest"
    local tag_name=$(curl -s "$url" | jq -r '.tag_name')

    # Update the file with the fetched tag
    if [[ -f "$file_path" ]]; then
        sed -i "s/newTag: [0-9.]\+/newTag: $tag_name/" "$file_path"
        echo "User tag '$tag_name' for $file_path"
    else
        echo "Error: File $file_path not found."
        exit 1
    fi
}

update_tag "virtool" "manifests/virtool/base/kustomization.yaml"
update_tag "virtool-ui" "manifests/ui/kustomization.yaml"

echo ""
echo "Workflows"
echo ""

for workflow_name in "build-index" "create-sample" "create-subtraction" "iimi" "nuvs" "pathoscope"; do
    url="https://api.github.com/repos/virtool/workflow-${workflow_name}/releases/latest"

    # Fetch the latest release tag name
    tag_name=$(curl -s "$url" | jq -r '.tag_name')

    # File to update
    file_path="manifests/workflows/${workflow_name}.yaml"

    # Update the file with the fetched tag
    if [[ -f "$file_path" ]]; then
        sed -i "s/${workflow_name}:[0-9.]\+/${workflow_name}:${tag_name}/" "$file_path"
        echo "Using tag '$tag_name' for $file_path"
    else
        echo "Error: File $file_path not found."
        exit 1
    fi
done