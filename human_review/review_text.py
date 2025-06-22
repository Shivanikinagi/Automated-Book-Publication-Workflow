import difflib
import re

def highlight_errors(text):
    # Highlight repeated words
    return re.sub(r'\b(\w+)( \1\b)+', r'[\1]', text)

def quality_check(text):
    if len(text) < 50 or "..." in text or re.search(r'\b(\w+)( \1){2,}\b', text):
        return False
    return True

def human_review(text, version):
    print(f"\n[Human Review] Version {version} ready for review.")
    print("Instruction examples: 'shorten sentences', 'add dramatic flair', 'make it sound cool', 'make it formal'")
    print("Preview (errors highlighted):\n", highlight_errors(text[:300]), "...\n")
    user_edit = input("Enter an edit instruction (or press Enter to keep as is): ").strip()
    if user_edit:
        # For demo, just append the instruction to the text
        edited_text = text + f"\n\n[Edit applied: {user_edit}]"
        show_diff(text, edited_text)
        return edited_text
    else:
        # Quality check if no edit
        if not quality_check(text):
            print("[Human Review] Warning: Text flagged as low quality. Please consider editing.")
        return text

def show_diff(original, edited):
    diff = difflib.unified_diff(
        original.splitlines(), edited.splitlines(),
        fromfile='Original', tofile='Edited', lineterm=''
    )
    print("\n[Diff] Changes after your edit:")
    print('\n'.join(diff))