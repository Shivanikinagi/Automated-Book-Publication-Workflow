from scraping.scrape_chapter import scrape_chapter
from ai_writer.spin_text import spin_chapter
from human_review.review_text import human_review
from storage.chromadb_handler import store_version
from retrieval.rl_search import retrieve_best_version
import os

def orchestrate_pipeline():
    print("🔎 Starting agentic pipeline...\n")

    print("Step 1: Scraping chapter...")
    chapter_text = scrape_chapter()
    if os.path.exists("screenshots/chapter.png"):
        print("✅ Screenshot saved at screenshots/chapter.png")
    else:
        print("❌ Screenshot not found!")

    print("\nStep 2: Spinning chapter with AI...")
    user_instruction = input("Enter any special instruction for the AI (e.g., 'make it simple', 'make it sound cool'): ").strip()
    spun_text, confidence = spin_chapter(chapter_text, user_instruction)
    print(f"✅ AI confidence score: {confidence:.2f}")

    version = 1
    current_text = spun_text
    while True:
        print(f"\n=== Review Iteration {version} ===")
        final_text = human_review(current_text, version)
        store_version(final_text, version=f"v{version}", author="Human Reviewer")
        print(f"✅ Version v{version} stored in ChromaDB.")
        print("\nDo you want another review iteration? (y/n): ")
        if input().lower() != 'y':
            break
        current_text = final_text
        version += 1

    print("\nStep 3: Retrieving best version...")
    result = retrieve_best_version("morning sea gates", user_instruction)
    print("\n📖 Best Retrieved Version:\n", result)

if __name__ == "__main__":
    orchestrate_pipeline()