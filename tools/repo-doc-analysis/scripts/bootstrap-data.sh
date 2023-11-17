#!/bin/bash
# For development and experiments we select a small number of ASF projects.
#-----------------------------------------------------------------------------------------------------------------------

clone_or_pull_github_repo() {
    local repository_url=$1
    local directory_name=$2

    if [ -d "$DOC_INSPECTION_WORKSPACE/$directory_name" ]; then
        echo "Directory '$directory_name' already exists. Performing a git pull."
        cd "$DOC_INSPECTION_WORKSPACE/$directory_name" || exit
        git pull
    else
        echo "Directory '$DOC_INSPECTION_WORKSPACE/$directory_name' does not exist. Performing a git clone."
        git clone "$repository_url" "$DOC_INSPECTION_WORKSPACE/$directory_name"
        cd "$DOC_INSPECTION_WORKSPACE/$directory_name" || exit
        git fetch
    fi
}

clone_or_pull_github_repo "https://github.com/apache/incubator-wayang" "incubator-wayang"

clone_or_pull_github_repo "https://github.com/apache/kafka" "kafka"

