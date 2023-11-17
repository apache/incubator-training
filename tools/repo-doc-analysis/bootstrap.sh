#!/bin/bash

source env.sh

pip install langchain==0.0.123 # https://github.com/hwchase17/langchain/releases
pip install openai
pip install faiss-cpu
pip install tiktoken

create_directory_if_not_exists() {
    local directory_name=$1

    if [ ! -d "$directory_name" ]; then
        mkdir "$directory_name"
        echo "Directory '$directory_name' created successfully."
    else
        echo "Directory '$directory_name' already exists."
    fi
}

create_directory_if_not_exists "$DOC_INSPECTION_WORKSPACE"
create_directory_if_not_exists "$DOC_INSPECTION_DATASTORE"

./scripts/bootstrap-data.sh