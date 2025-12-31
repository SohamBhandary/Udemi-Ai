from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI


client = OpenAI(
    api_key="your-api-key",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


Vector_db = QdrantVectorStore.from_existing_collection(
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="rag"
)

user_query = input("Ask Something >>>> ")


search_results = Vector_db.similarity_search(query=user_query, k=5)

context = "\n\n\n".join([
    f"Page Content: {result.page_content[:500]}...\nPage Number: {result.metadata.get('page_label','Unknown')}\nFile Location: {result.metadata.get('source','Unknown')}"
    for result in search_results
])

SYSTEM_PROMPT = f"""
You are a helpful AI Assistant who answers user queries based on the available context retrieved from a PDF file along with page_contents and page number.

You should only answer the user based on the following context and navigate the user to open the right page number to know more.

Context:
{context}
"""


response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_query},
    ]
)

print(f"🤖: {response.choices[0].message.content}")
