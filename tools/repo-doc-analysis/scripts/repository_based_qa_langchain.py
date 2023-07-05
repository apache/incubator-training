# -*- coding: utf-8 -*-

#
# This script is inspired by the work of Quy Tang:
#    https://medium.com/singapore-gds/integrating-chatgpt-with-internal-knowledge-base-and-question-answer-platform-36a3283d6334
#


import os
from getpass import getpass

#import project_metadata.kafka as pmd
import project_metadata.incubator_wayang as pmd
import question_sets as qs


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
chunk_size_limit = 1500
max_chunk_overlap = 100

repo_path = pathlib.Path(os.path.join(pmd.DOCS_FOLDER, pmd.REPO_DOCUMENTS_PATH))
document_files = list(repo_path.glob(name_filter))

print( document_files )

def convert_path_to_doc_url(doc_path):
  # Convert from relative path to actual document url
  return re.sub(f"{pmd.DOCS_FOLDER}/{pmd.REPO_DOCUMENTS_PATH}/(.*)\.[\w\d]+", f"{pmd.DOCUMENT_BASE_URL}/\\1", str(doc_path))

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

key = os.environ["OPENAI_API_KEY"]
if key is None:
    os.environ["OPENAI_API_KEY"] = getpass("Paste your OpenAI API key here and hit enter:")
else:
    print( "> use OpenAI API-key from ENV variable OPENAI_API_KEY.")

embeddings = OpenAIEmbeddings()
vector_store = FAISS.from_documents(split_docs, embeddings)


"""## (Optional) Save vector store to files and download/save in another location for reuse"""

vector_store.save_local(pmd.DATA_STORE_DIR)
# Download the files `$DATA_STORE_DIR/index.faiss` and `$DATA_STORE_DIR/index.pkl` to local

"""#### To load the Vector Store from files:"""

# Upload the files `$DATA_STORE_DIR/index.faiss` and `$DATA_STORE_DIR/index.pkl` to local
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

if os.path.exists(pmd.DATA_STORE_DIR):
  vector_store = FAISS.load_local(
      pmd.DATA_STORE_DIR,
      OpenAIEmbeddings()
  )
else:
  print(f"Missing files. Upload index.faiss and index.pkl files to {pmd.DATA_STORE_DIR} directory first")

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
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, max_tokens=1500)  # Modify model_name if you have access to GPT-4
chain = RetrievalQAWithSourcesChain.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vector_store.as_retriever(),
    return_source_documents=True,
    chain_type_kwargs=chain_type_kwargs
)

def print_problem(query,ex,f):
    output_text = f"""\n-------------------------------------------------------------------------------
  ### Question:
  -------------------------------------------------------------------------------\n
  {query}
  -------------------------------------------------------------------------------\n
  {ex}
  """
    f.write( output_text )
    # print( output_text )

def print_result(result, query, f):
  output_text = """
## Question:
{0}

## Answer:
{1}

### Sources:
{2}
  
#### All relevant sources:
+ {3}
""".format(
      query,
      result['answer'],
      result['sources'],
      '\n+ '.join(list(set([doc.metadata['source'] for doc in result['source_documents']]))),
  )

  f.write( output_text )
  # print( output_text )

import logging

logging.getLogger("openai").setLevel(logging.DEBUG) # logging.INFO or logging.DEBUG

"""#### Use the chain to query"""

QUESTION_SET = qs.queryies2

fa = open( f"./../reports/{pmd.PROJECT_FOLDER}/answers_{QUESTION_SET[1]}.md", "w")
fp = open( f"./../reports/{pmd.PROJECT_FOLDER}/problems_{QUESTION_SET[1]}.md", "w")

for q in QUESTION_SET[0]:

    try:
        result = chain(q)

        print_result(result, q, fa)

    except Exception as ex:
        print_problem(q, ex, fp)

fa.close()
fp.close()

