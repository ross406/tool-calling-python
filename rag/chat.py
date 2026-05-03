from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI

load_dotenv()

openai_client = OpenAI()

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large",   
)

vector_db = QdrantVectorStore.from_existing_collection(
     url="http://localhost:6333",
     collection_name="node_pdf",
     embedding=embeddings,
)

# Take the user input

user_query = input("What is your question about the PDF? ")

#Relevent chunks from the vector database
search_results = vector_db.similarity_search(query=user_query)

context = "\n\n\n".join([f"Page Content:{result.page_content}\nPage Number: {result.metadata['page_label']}\nFile Location: {result.metadata['source']}" for result in search_results])

SYSTEM_PROMPT = f"""You are an assistant that answers questions about the content of a PDF document.
 Use the following chunks of information from the PDF to answer the question along with page_contents and page number.

 you should only answer based on the following context and navigate the user to the page number if needed. 

 Context:{context}
  """

response = openai_client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_query}
    ]
)

print("Answer:", response.choices[0].message.content)