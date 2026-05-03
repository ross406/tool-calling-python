from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

from dotenv import load_dotenv


load_dotenv()


pdf_path = Path(__file__).parent / "node.pdf"

# Load this PDF into a vector database and create an agent that can answer questions about it.

loader = PyPDFLoader(file_path=pdf_path)
docs = loader.load()

# Split the document into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=400)

chunks = text_splitter.split_documents(documents=docs)


embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large",   
)

vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embeddings,
    url="http://localhost:6333",
    collection_name="node_pdf"
)

print("Indexing complete!")