import chromadb
import os

def store_version(content, version, author):
    os.makedirs("db", exist_ok=True)
    client = chromadb.PersistentClient(path="db")
    collection = client.get_or_create_collection(name="chapters")

    collection.add(
        documents=[content],
        ids=[version],
        metadatas=[{"author": author}]
    )

def fetch_versions():
    client = chromadb.PersistentClient(path="db")
    collection = client.get_or_create_collection(name="chapters")
    return collection.get()