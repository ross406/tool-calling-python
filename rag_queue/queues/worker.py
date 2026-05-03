from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
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

def process_query(query:str):
    print(f"Searching chunks for query: {query}")

    search_results = vector_db.similarity_search(query=query)

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
            {"role": "user", "content": query}
        ]
    ) 

    print("Answer:", response.choices[0].message.content)
    
    return response.choices[0].message.content