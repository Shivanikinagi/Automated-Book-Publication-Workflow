import os
from transformers import pipeline
import re

def spin_chapter():
    print("Starting spin_chapter...")
    # Initialize T5 pipeline for CPU
    paraphraser = pipeline("text2text-generation", model="t5-small", device=-1)  # -1 for CPU
    print("T5 model loaded.")

    # Read scraped chapter text
    try:
        with open("data/chapter_original.txt", "r", encoding="utf-8") as f:
            content = f.read()
        print("Read chapter_original.txt.")
    except FileNotFoundError:
        raise FileNotFoundError("Original chapter text not found. Run scrape_chapter.py first.")

    if not content.strip():
        raise ValueError("Scraped chapter content is empty.")

    # Clean content
    content = re.sub(r'\[\d+\]', '', content)  # Remove [1], [2], etc.
    content = re.sub(r'\s+', ' ', content).strip()  # Normalize whitespace
    content = ''.join(c for c in content if c.isprintable())  # Remove non-printable chars
    print("Content cleaned.")

    # Split content into chunks
    max_length = 150  # Optimized for t5-small
    chunks = [content[i:i+max_length] for i in range(0, len(content), max_length)]
    spun_text = ""
    print(f"Processing {len(chunks)} chunks...")

    for i, chunk in enumerate(chunks):
        prompt = f"paraphrase: {chunk}"
        try:
            result = paraphraser(prompt, max_length=200, num_return_sequences=1, do_sample=False)
            generated_text = result[0]["generated_text"].strip()
            if generated_text.startswith("paraphrase:"):
                generated_text = generated_text[len("paraphrase:"):].strip()
            spun_text += generated_text + " "
            print(f"Processed chunk {i+1}/{len(chunks)}")
        except Exception as e:
            print(f"Failed to process chunk {i+1}: {e}")
            spun_text += chunk + " "  # Fallback to original

    # Save spun text
    os.makedirs("data", exist_ok=True)
    with open("data/chapter_spun_v1.txt", "w", encoding="utf-8") as f:
        f.write(spun_text.strip())
    print("Saved chapter_spun_v1.txt.")

    return spun_text.strip()