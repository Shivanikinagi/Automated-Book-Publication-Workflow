import chromadb
import re

def readability_score(text):
    if len(text) < 50 or re.search(r'\b(\w+)( \1){2,}\b', text):
        return 0.2
    sentences = max(1, text.count('.') + text.count('!') + text.count('?'))
    words = len(text.split())
    avg_len = words / sentences
    if avg_len < 5 or avg_len > 25:
        return 0.3  # Penalize too short/long sentences
    return min(1.0, avg_len / 20)

def style_alignment_score(text, instruction):
    if "cool" in instruction.lower() and any(word in text.lower() for word in ["awesome", "epic", "vibe", "lit"]):
        return 1.0
    if "dramatic" in instruction.lower() and any(word in text.lower() for word in ["suddenly", "unfolded", "storm"]):
        return 1.0
    if "simple" in instruction.lower() and len(text.split()) < 100:
        return 1.0
    return 0.5

def retrieve_best_version(query, instruction=""):
    client = chromadb.PersistentClient(path="db")
    collection = client.get_or_create_collection(name="chapters")
    print(f"[ChromaDB] Querying for: {query}")
    results = collection.query(
        query_texts=[query],
        n_results=5
    )
    best_doc = None
    best_score = -1
    for idx, doc in enumerate(results.get('documents', [[]])[0]):
        score = results.get('distances', [[0]])[0][idx]
        readability = readability_score(doc)
        style = style_alignment_score(doc, instruction)
        combined = (1 - score) * 0.5 + readability * 0.3 + style * 0.2
        print(f"[ChromaDB] Candidate {idx+1}: similarity={1-score:.2f}, readability={readability:.2f}, style={style:.2f}, combined={combined:.2f}")
        if combined > best_score:
            best_score = combined
            best_doc = doc
    if best_doc:
        print(f"[ChromaDB] Best version chosen by combined score: {best_score:.2f}")
        return best_doc
    print("[ChromaDB] No matching version found.")
    return "No matching version found."