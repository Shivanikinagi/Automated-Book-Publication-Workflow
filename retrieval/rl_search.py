import chromadb

def retrieve_best_version(query):
    client = chromadb.PersistentClient(path="db")
    collection = client.get_or_create_collection(name="chapters")

    results = collection.query(
        query_texts=[query],
        n_results=1
    )

    if results['documents'] and results['documents'][0]:
        return results['documents'][0][0]
    return "No matching version found."