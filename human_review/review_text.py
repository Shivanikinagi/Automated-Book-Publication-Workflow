import os

def human_review(spun_text, iteration):
    print(f"\n=== Review Iteration {iteration} ===")
    print(f"\n📜 AI-Generated Chapter (Iteration {iteration}):\n")
    # Show first 500 characters or full text if shorter
    preview_length = 500
    print(spun_text[:preview_length] + "..." if len(spun_text) > preview_length else spun_text)
    print(f"\nPlease enter your edits for iteration {iteration} (or press Enter to accept as-is):\n")
    edited_text = input()

    final_text = edited_text.strip() if edited_text.strip() else spun_text
    os.makedirs("data", exist_ok=True)
    with open(f"data/chapter_final_v{iteration}.txt", "w", encoding="utf-8") as f:
        f.write(final_text)

    return final_text