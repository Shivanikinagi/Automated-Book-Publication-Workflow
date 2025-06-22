import chromadb
import re
from human_review.review_text import quality_check, human_review

def store_version(content, version, author):
    if not quality_check(content):
        print("[ChromaDB] Warning: Text flagged as low quality. Please edit before storing.")
        edit = input("Edit now? (y/n): ")
        if edit.lower() == 'y':
            content = human_review(content, version)
            if not quality_check(content):
                print("[ChromaDB] Still low quality. Not storing.")
                return
        else:
            print("[ChromaDB] Not storing due to quality issues.")
            return
    client = chromadb.Client()
    collection = client.get_or_create_collection(name="chapters")
    collection.add(
        documents=[content],
        ids=[version],
        metadatas=[{"author": author}]
    )
    print(f"[ChromaDB] Stored version '{version}' by {author}")