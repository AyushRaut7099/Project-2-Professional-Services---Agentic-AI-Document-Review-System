import chromadb
chroma_client = chromadb.PersistentClient(path="chroma_db")
collection = chroma_client.get_or_create_collection(
    name="pdf_data"
)
def clear_database():
    all_data = collection.get()
    if all_data["ids"]:
        collection.delete(ids=all_data["ids"])
def store_chunks(chunks, embeddings):
    clear_database()
    for i in range(len(chunks)):
        collection.add(
            documents=[chunks[i]],
            embeddings=[embeddings[i]],
            ids=[str(i)]
        )