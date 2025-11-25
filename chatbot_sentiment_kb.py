#!/usr/bin/env python3
"""
Advanced rule-based chatbot with:
 - simple sentiment analysis (lexicon-based)
 - emotion detection (keyword mapping)
 - JSON knowledge base with fuzzy matching
No external libraries required.
"""

import json
import re
import random
import os
from difflib import get_close_matches
from collections import Counter

# -----------------------------
# Simple Sentiment Lexicons
# -----------------------------
POS_WORDS = {
    "good","great","awesome","fantastic","love","liked","happy","nice","excellent",
    "amazing","wonderful","best","positive","pleased","enjoy","enjoyed","yay","yay!"
}
NEG_WORDS = {
    "bad","terrible","awful","hate","hated","sad","angry","upset","worst","poor",
    "negative","disappointed","disappointing","angry","ugh","sucks"
}

# -----------------------------
# Emotion keyword mapping
# -----------------------------
EMOTION_KEYWORDS = {
    "joy": {"happy","joy","delighted","excited","glad","pleased","yay","awesome"},
    "sadness": {"sad","unhappy","down","depressed","blue","sorrow","mourn"},
    "anger": {"angry","mad","furious","irate","annoyed","hate","hated"},
    "fear": {"scared","afraid","fear","terrified","panic","anxious"},
    "surprise": {"surprised","wow","shocked","amazed"},
    "love": {"love","loving","adore","cherish"}
}

# -----------------------------
# Rule-based intents
# -----------------------------
INTENTS = {
    "greeting": {
        "patterns": [r"\bhello\b", r"\bhi\b", r"\bhey\b", r"\bgood morning\b", r"\bgood evening\b"],
        "responses": ["Hello! How can I help you today?", "Hi there — what can I do for you?", "Hey! Ask me anything."]
    },
    "goodbye": {
        "patterns": [r"\bbye\b", r"\bgoodbye\b", r"\bsee you\b", r"\bexit\b", r"\bquit\b"],
        "responses": ["Goodbye! Take care.", "See you later!", "It was nice talking to you."]
    },
    "thanks": {
        "patterns": [r"\bthanks\b", r"\bthank you\b", r"\bthx\b"],
        "responses": ["You're welcome!", "No problem — happy to help.", "Anytime!"]
    },
    "how_are_you": {
        "patterns": [r"how are you", r"how's it going", r"how are things"],
        "responses": ["I'm a bot, but I'm running smoothly!", "All good here — ready to help you."]
    },
    "help": {
        "patterns": [r"\bhelp\b", r"\bassist\b", r"\bsupport\b", r"what can you do"],
        "responses": [
            "I can answer common questions, detect basic sentiment in your text, and fetch answers from a small knowledge base.",
            "Try asking me about the project tasks (image resizer, Flask app, data analysis), or say how you're feeling."
        ]
    }
}

# -----------------------------
# Helper utilities
# -----------------------------
def normalize(text: str) -> str:
    """Lowercase and remove punctuation (simple normalization)."""
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def tokenize(text: str):
    return normalize(text).split()

# -----------------------------
# Sentiment / Emotion functions
# -----------------------------
def detect_sentiment(text: str) -> dict:
    """
    Return a simple sentiment analysis result:
    - polarity: positive / negative / neutral
    - score: (#pos - #neg)
    - pos_count, neg_count
    """
    tokens = tokenize(text)
    pos_count = sum(1 for t in tokens if t in POS_WORDS)
    neg_count = sum(1 for t in tokens if t in NEG_WORDS)
    score = pos_count - neg_count
    if score > 0:
        polarity = "positive"
    elif score < 0:
        polarity = "negative"
    else:
        polarity = "neutral"
    return {"polarity": polarity, "score": score, "pos": pos_count, "neg": neg_count}

def detect_emotions(text: str) -> dict:
    """
    Returns a mapping of detected emotion -> count. Might return multiple detected emotions.
    """
    tokens = set(tokenize(text))
    found = {}
    for emo, kwset in EMOTION_KEYWORDS.items():
        matches = tokens.intersection(kwset)
        if matches:
            found[emo] = len(matches)
    return found  # empty dict if none

# -----------------------------
# Knowledge Base (JSON) loader & search
# -----------------------------
KB_FILENAME = "knowledge_base.json"

def load_kb(filename=KB_FILENAME):
    if not os.path.exists(filename):
        print(f"[KB] Warning: {filename} not found. Knowledge base disabled.")
        return []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            # ensure list of dicts with 'question' and 'answer'
            valid = [entry for entry in data if "question" in entry and "answer" in entry]
            print(f"[KB] Loaded {len(valid)} entries from {filename}.")
            return valid
    except Exception as e:
        print(f"[KB] Error loading {filename}: {e}")
        return []

def find_in_kb(user_input: str, kb_data, cutoff=0.6):
    """
    Try to find the best KB match. Uses difflib's get_close_matches on normalized question strings.
    Returns the answer if found, or None.
    """
    if not kb_data:
        return None
    user_norm = normalize(user_input)
    questions = [normalize(entry["question"]) for entry in kb_data]
    # quick token overlap check first (rank by overlap)
    user_tokens = set(user_norm.split())
    overlap_scores = []
    for idx, q in enumerate(questions):
        q_tokens = set(q.split())
        overlap = len(user_tokens & q_tokens)
        overlap_scores.append((overlap, idx))
    # pick best overlap if any positive overlap
    overlap_scores.sort(reverse=True)
    best_overlap, best_idx = overlap_scores[0]
    if best_overlap > 0:
        # check ratio of overlap to question length
        q_tokens = set(questions[best_idx].split())
        ratio = best_overlap / max(1, len(q_tokens))
        if ratio >= cutoff:  # strong match by overlap
            return kb_data[best_idx]["answer"]
    # fallback to difflib fuzzy match using whole strings
    matches = get_close_matches(user_norm, questions, n=1, cutoff=0.7)
    if matches:
        matched_q = matches[0]
        matched_idx = questions.index(matched_q)
        return kb_data[matched_idx]["answer"]
    return None

# -----------------------------
# Intent matching
# -----------------------------
def match_intent(user_input: str):
    """Return an intent key if any pattern matches, else None."""
    text = user_input.lower()
    for intent, data in INTENTS.items():
        for patt in data["patterns"]:
            if re.search(patt, text):
                return intent
    return None

def intent_response(intent_key: str):
    return random.choice(INTENTS[intent_key]["responses"])

# -----------------------------
# Chat loop
# -----------------------------
def main():
    kb_data = load_kb()
    print("ChatBuddy: Hi! I'm ChatBuddy (rule + sentiment + KB). Type 'bye' to exit.")
    print("Tip: Ask project questions (e.g. 'how to resize images') or tell me how you feel.")
    while True:
        try:
            user = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nChatBuddy: Bye!")
            break

        if not user:
            print("ChatBuddy: Say something — I'm listening.")
            continue

        # quick exit
        if re.search(r"\b(bye|goodbye|exit|quit)\b", user, re.IGNORECASE):
            print("ChatBuddy: Goodbye — take care!")
            break

        # 1) Check knowledge base first (prefer factual answers)
        kb_answer = find_in_kb(user, kb_data)
        if kb_answer:
            # still provide sentiment/emotion feedback optionally
            sentiment = detect_sentiment(user)
            emotions = detect_emotions(user)
            print(f"ChatBuddy (KB): {kb_answer}")
            # short feedback
            if sentiment["polarity"] != "neutral":
                print(f"[Sentiment detected: {sentiment['polarity']} (score={sentiment['score']})]")
            if emotions:
                # pick highest count emotion or list them
                detected = ", ".join(f"{k}" for k in emotions.keys())
                print(f"[Emotion(s) detected: {detected}]")
            continue

        # 2) Intent matching (greeting/help/etc.)
        intent = match_intent(user)
        if intent:
            print("ChatBuddy:", intent_response(intent))
            # show sentiment optionally when user asks "how are you" etc
            continue

        # 3) Sentiment & emotion analysis + fallback response
        sentiment = detect_sentiment(user)
        emotions = detect_emotions(user)

        if sentiment["polarity"] == "negative":
            # empathetic reply
            if emotions.get("sadness"):
                print("ChatBuddy: I'm sorry to hear that. Do you want to talk about it?")
            elif emotions.get("anger"):
                print("ChatBuddy: I understand that you're upset. Want to vent or get tips to calm down?")
            else:
                print("ChatBuddy: That sounds rough. Want some suggestions to help?")
            # also show small sentiment summary
            print(f"[Sentiment: negative (score={sentiment['score']})]")
            continue
        elif sentiment["polarity"] == "positive":
            if emotions.get("joy") or emotions.get("love"):
                print("ChatBuddy: That's wonderful to hear! Glad you're feeling good :)")
            else:
                print("ChatBuddy: Nice! Happy to hear that.")
            print(f"[Sentiment: positive (score={sentiment['score']})]")
            continue
        else:
            # neutral & unknown: fallback small talk / explanation
            # try keyword-based quick answers
            # small knowledge quick answers for some keywords
            if re.search(r"\b(resize|image|pillow|pil)\b", user, re.IGNORECASE):
                print("ChatBuddy: For resizing images in Python use PIL/Pillow: Image.open(path).resize((w,h)).save(out).")
                continue
            if re.search(r"\b(flask|api|endpoint)\b", user, re.IGNORECASE):
                print("ChatBuddy: Flask is a minimal Python web framework. Use @app.route to define endpoints.")
                continue
            # final fallback
            fallback_phrases = [
                "I'm not sure yet — can you rephrase?",
                "I don't have an exact answer for that, but I can try to help.",
                "Interesting — tell me more or ask a different way."
            ]
            print("ChatBuddy:", random.choice(fallback_phrases))

if __name__ == "__main__":
    main()
