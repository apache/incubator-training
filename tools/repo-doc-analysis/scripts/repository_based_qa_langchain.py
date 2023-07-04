# -*- coding: utf-8 -*-

#
# This script is inspired by the work of Quy Tang:
#    https://medium.com/singapore-gds/integrating-chatgpt-with-internal-knowledge-base-and-question-answer-platform-36a3283d6334
#


import os
from getpass import getpass


REPO_URL = "https://github.com/GovTechSG/developer.gov.sg"  # Source URL
DOCS_FOLDER = "./../docs-main/incubator-wayang/"  # Folder to check out to
REPO_DOCUMENTS_PATH = "wayang-docs/"  # Set to "" to index the whole data folder
DOCUMENT_BASE_URL = "https://www.developer.tech.gov.sg/products/categories/devops/ship-hats"  # Actual URL
DATA_STORE_DIR = "data-store"

"""## Build the datastore
*(Skip to next section to load data store from files if it has been saved locally to save cost of embeddings)*


"""### Load documents and split them into chunks for conversion to embeddings"""

import os
import pathlib
import re

from langchain.docstore.document import Document
from langchain.document_loaders import TextLoader

from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

name_filter = "**/*.md"
separator = "\n### "  # This separator assumes Markdown docs from the repo uses ### as logical main header most of the time
chunk_size_limit = 1000
max_chunk_overlap = 20

repo_path = pathlib.Path(os.path.join(DOCS_FOLDER, REPO_DOCUMENTS_PATH))
document_files = list(repo_path.glob(name_filter))

print( document_files )

def convert_path_to_doc_url(doc_path):
  # Convert from relative path to actual document url
  return re.sub(f"{DOCS_FOLDER}/{REPO_DOCUMENTS_PATH}/(.*)\.[\w\d]+", f"{DOCUMENT_BASE_URL}/\\1", str(doc_path))

documents = [
    Document(
        page_content=open(file, "r").read(),
        metadata={"source": convert_path_to_doc_url(file)}
    )
    for file in document_files
]

print( len(documents) )

text_splitter = CharacterTextSplitter(separator=separator, chunk_size=chunk_size_limit, chunk_overlap=max_chunk_overlap)
split_docs = text_splitter.split_documents(documents)

"""### (Optional) Check estimated tokens and costs"""


import tiktoken
# create a GPT-4 encoder instance
enc = tiktoken.encoding_for_model("gpt-4")

total_word_count = sum(len(doc.page_content.split()) for doc in split_docs)
total_token_count = sum(len(enc.encode(doc.page_content)) for doc in split_docs)

print(f"\nTotal word count: {total_word_count}")
print(f"\nEstimated tokens: {total_token_count}")
print(f"\nEstimated cost of embedding: ${total_token_count * 0.0004 / 1000}")

"""### Create Vector Store using OpenAI"""


os.environ["OPENAI_API_KEY"] = getpass("Paste your OpenAI API key here and hit enter:")

embeddings = OpenAIEmbeddings()
vector_store = FAISS.from_documents(split_docs, embeddings)

"""### Verify content of Vector Store with a sample query"""

from IPython.display import display, Markdown

search_result = vector_store.similarity_search_with_score("What is SHIP-HATS?")
search_result

line_separator = "\n"# {line_separator}Source: {r[0].metadata['source']}{line_separator}Score:{r[1]}{line_separator}
display(Markdown(f"""
## Search results:{line_separator}
{line_separator.join([
  f'''
  ### Source:{line_separator}{r[0].metadata['source']}{line_separator}
  #### Score:{line_separator}{r[1]}{line_separator}
  #### Content:{line_separator}{r[0].page_content}{line_separator}
  '''
  for r in search_result
])}
"""))

"""## (Optional) Save vector store to files and download/save in another location for reuse"""

vector_store.save_local(DATA_STORE_DIR)
# Download the files `$DATA_STORE_DIR/index.faiss` and `$DATA_STORE_DIR/index.pkl` to local

"""#### To load the Vector Store from files:"""

# Upload the files `$DATA_STORE_DIR/index.faiss` and `$DATA_STORE_DIR/index.pkl` to local
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

if os.path.exists(DATA_STORE_DIR):
  vector_store = FAISS.load_local(
      DATA_STORE_DIR,
      OpenAIEmbeddings()
  )
else:
  print(f"Missing files. Upload index.faiss and index.pkl files to {DATA_STORE_DIR} directory first")

"""## Query using the vector store with ChatGPT integration
### Set up the chat model and specific prompt
"""

from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

system_template="""Use the following pieces of context to answer the users question.
Take note of the sources and include them in the answer in the format: "SOURCES: source1 source2", use "SOURCES" in capital letters regardless of the number of sources.
If you don't know the answer, just say that "I don't know", don't try to make up an answer.
----------------
{summaries}"""
messages = [
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template("{question}")
]
prompt = ChatPromptTemplate.from_messages(messages)

from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQAWithSourcesChain

chain_type_kwargs = {"prompt": prompt}
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, max_tokens=256)  # Modify model_name if you have access to GPT-4
chain = RetrievalQAWithSourcesChain.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vector_store.as_retriever(),
    return_source_documents=True,
    chain_type_kwargs=chain_type_kwargs
)

from IPython.display import display, Markdown
def print_result(result):
  output_text = f"""### Question:
  {query}
  ### Answer:
  {result['answer']}
  ### Sources:
  {result['sources']}
  ### All relevant sources:
  {' '.join(list(set([doc.metadata['source'] for doc in result['source_documents']])))}
  """
  display(Markdown(output_text))

"""#### Use the chain to query"""

query = "What is SHIP-HATS?"
result = chain(query)
print_result(result)

"""Turn on debugging to see the OpenAI requests"""

import logging

logging.getLogger("openai").setLevel(logging.DEBUG) # logging.INFO or logging.DEBUG

query = "What is SHIP-HATS?"
result = chain(query)
print_result(result)

"""Print result again without rerunning"""

print_result(result)