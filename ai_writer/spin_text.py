import random
import re

def style_guideline(instruction):
    if "cool" in instruction.lower():
        return "Use vivid metaphors, concise phrasing, and modern slang."
    if "dramatic" in instruction.lower():
        return "Add suspenseful language and emotional intensity."
    if "formal" in instruction.lower():
        return "Use formal tone and complex sentence structure."
    if "simple" in instruction.lower():
        return "Use short, clear sentences and basic vocabulary."
    return ""

def fake_llm_api(prompt, instruction=""):
    text = prompt
    if "simple" in instruction.lower():
        # Simulate simplification: short sentences, basic words
        text = re.sub(r'\b(morning|dawn|commence|proceed|inhabited)\b', 'day', text, flags=re.I)
        text = re.sub(r'[,;:]', '.', text)
        text = '. '.join([s.strip() for s in text.split('.') if len(s.split()) < 12])
    elif "cool" in instruction.lower():
        text = text.replace("said", "was like,").replace("walked", "vibed")
    elif "dramatic" in instruction.lower():
        text = text.replace("said", "exclaimed").replace("walked", "stormed")
    elif "formal" in instruction.lower():
        text = text.replace("you", "one").replace("I", "the author")
    return text.strip()

def advanced_cleanup(text):
    # Remove repeated words/phrases
    text = re.sub(r'\b(\w+)( \1\b)+', r'\1', text)
    # Remove incomplete sentences (less than 3 words or not ending with punctuation)
    sentences = [s.strip() for s in re.split(r'[.!?]', text) if len(s.split()) > 2]
    text = '. '.join(sentences) + '.'
    # Remove artifacts and extra spaces
    text = re.sub(r'(?i)\bparaphrase:\s*', '', text)
    text = re.sub(r'\.{2,}', '.', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def estimate_confidence(text):
    if len(text) < 50 or re.search(r'\b(\w+)( \1){2,}\b', text):
        return random.uniform(0.5, 0.7)
    return random.uniform(0.85, 0.99)

def spin_chapter(text, user_instruction=None):
    guideline = style_guideline(user_instruction or "")
    prompt = f"Paraphrase the following text. Instruction: {user_instruction or ''} {guideline}\n{text}"
    paraphrased = fake_llm_api(prompt, user_instruction or "")
    cleaned = advanced_cleanup(paraphrased)
    confidence = estimate_confidence(cleaned)
    print(f"[AI Writer] Paraphrased text generated with confidence {confidence:.2f}")
    return cleaned, confidence