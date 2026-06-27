import chromadb #chromadb storing vectors(numbers)
from backend.embeddings import get_embedding #function to get the embedding vector for a given text chunk from embeddings.py
chroma_client = chromadb.PersistentClient(path="chroma_db") #connecting to chromadb database located at chroma_db folder
collection = chroma_client.get_collection(name="pdf_data") 
def retrieve_chunks(query, top_k=3): #fxn to retrieve relevant text chunks based on a user query, using the embedded stored in chromadb 
    query_embedding = get_embedding(query) #converting the user query into an embedding vector using the same get_embeddedings fucntion
    results = collection.query( 
        query_embeddings=[query_embedding], 
        n_results=top_k #number of top relevant chunks to retrieve based on cosine similarity between query embedding and stored chunk embeddings
    )
    return results