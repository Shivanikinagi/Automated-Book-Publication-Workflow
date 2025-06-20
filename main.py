from scraping.scrape_chapter import scrape_chapter
from ai_writer.spin_text import spin_chapter
from human_review.review_text import human_review
from storage.chromadb_handler import store_version
from retrieval.rl_search import retrieve_best_version
import os 

print("Scraping chapter...")
scrape_chapter()

print("Spinning chapter with AI...")
spun_text = spin_chapter()

version = 1
current_text = spun_text
while True:
    print(f"\n=== Review Iteration {version} ===")
    final_text = human_review(current_text, version)
    store_version(final_text, version=f"v{version}", author="Human Reviewer")
    print("\nDo you want another review iteration? (y/n): ")
    if input().lower() != 'y':
        break
    current_text = final_text
    version += 1

print("\nRetrieving best version...")
result = retrieve_best_version("morning sea gates")
print("\n📖 Best Retrieved Version:\n", result)