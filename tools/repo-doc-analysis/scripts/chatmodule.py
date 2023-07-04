# -*- coding: utf-8 -*-

import sys
import os

sys.path.insert(0,'.')

from flask import Flask, render_template, redirect, request, session, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from getpass import getpass

os.environ["OPENAI_API_KEY"] = getpass("Paste your OpenAI API key here and hit enter:")

print( "> Setup ChatGPT client environment ... " )

REPO_URL = "https://github.com/GovTechSG/developer.gov.sg"  # Source URL
DOCS_FOLDER = "docs-main"  # Folder to check out to
REPO_DOCUMENTS_PATH = ""  # Set to "" to index the whole data folder
DOCUMENT_BASE_URL = "https://www.developer.tech.gov.sg/products/categories/devops/ship-hats"  # Actual URL
DATA_STORE_DIR = "data-store"
#DATA_BASE_DIR = "./../temp/"
DATA_BASE_DIR = "./"
DOCS_FOLDER = "docs-main"  # Folder to check out to

import os
import pathlib
import re

from langchain.docstore.document import Document
from langchain.document_loaders import TextLoader

from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

name_filter = "**/*.adoc"
separator = "\n### "  # This separator assumes Markdown docs from the repo uses ### as logical main header most of the time
chunk_size_limit = 1000
max_chunk_overlap = 20


"""#### To load the Vector Store from files:"""
# Upload the files `$DATA_STORE_DIR/index.faiss` and `$DATA_STORE_DIR/index.pkl` to local

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

DATA_DIR = DATA_BASE_DIR + DATA_STORE_DIR

print("> " + os.getcwd() + " ... LOCATION for reading the index.")
print(f"> Try to load vector store ... <{DATA_DIR}>")

DATA_DIR = DATA_BASE_DIR + DATA_STORE_DIR
if os.path.exists( DATA_DIR ):
    vector_store = FAISS.load_local(
        DATA_DIR,
        OpenAIEmbeddings()
    )
    print("> Vector store has been loaded successfully.")
else:
    print(f"Missing files. Upload index.faiss and index.pkl files to {DATA_DIR} directory first")



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

domain_url = None

def get_formated_result( result, query):
    i = 1

    sl = " Sources:\n"
    for doc in result['source_documents']:
        sl = ' \n * ' + str(i) + " " + doc.metadata['source']

    output_text = f"""
### Question: 
{query}
      
### Answer: 
{result['answer']}
      
### Sources: 
{result['sources']}
      
### All relevant sources:
{sl}
"""
    return output_text

def print_result(result, query):
    get_formated_result( result, query )
    print( output_text )



"""#### Use the chain to query"""
def query_doc_chain( query = None ):

    print( "### >>> " + query )

    if query == None:
        query = "Which MySQL version is used by SaaS platform?"

    result = chain(query)

    text_result = get_formated_result(result,query)

    print( text_result )




if __name__ == '__main__':

    result = query_doc_chain( "What is SHIP-HATS?" )

    print( "\nDone." )