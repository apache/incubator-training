import os

doc_inspection_datastore = os.getenv('DOC_INSPECTION_DATASTORE')

if doc_inspection_datastore:
    print(f"Value of DOC_INSPECTION_DATASTORE is: {doc_inspection_datastore}")
else:
    print("DOC_INSPECTION_DATASTORE is not set.")
    exit(-1)

doc_inspection_workspace = os.getenv('DOC_INSPECTION_WORKSPACE')

if doc_inspection_workspace:
    print(f"Value of DOC_INSPECTION_WORKSPACE is: {doc_inspection_workspace}")
else:
    print("DOC_INSPECTION_WORKSPACE is not set.")
    exit(-1)

PROJECT_FOLDER = "kafka"
REPO_URL = "https://github.com/apache/kafka"  # Source URL
DOCS_FOLDER = f"{doc_inspection_workspace}/kafka/"  # Folder to check out to
REPO_DOCUMENTS_PATH = ""  # Set to "" to index the whole data folder
DOCUMENT_BASE_URL = "https://github.com/apache/kafka"  # Actual URL
DATA_STORE_DIR = f"{doc_inspection_datastore}/kafka"

print( "> Inspect Kafka repository ...")
