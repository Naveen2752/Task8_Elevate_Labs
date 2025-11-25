# Task8_Elevate_Labs

# 🧠 Advanced Python Chatbot

### **Rule-Based Chatbot + Sentiment Analysis + Emotion Detection + JSON Knowledge Base**

This project contains a fully functional Python chatbot that combines **rule-based logic**, **emotion detection**, and a **JSON-driven knowledge base** to deliver smart, human-like replies — without using any external machine-learning libraries.

It’s a perfect demonstration of:

* Python programming
* NLP basics
* Chatbot logic design
* JSON-based knowledge storage
* Sentiment & emotion analysis

Ideal for internships, resumes, and portfolio proof-of-skills.

---

## 🚀 Features

### ✅ **1. Rule-Based Intent Recognition**

Uses regex patterns to respond to:

* Greetings
* Goodbyes
* Help queries
* Thanks
* Small-talk questions (“How are you?”, “What can you do?”)

### ✅ **2. Sentiment Analysis (Lexicon-Based)**

Detects whether user input is:

* Positive
* Negative
* Neutral

Based on word-level polarity scores.

### ✅ **3. Emotion Detection**

Understands emotional tone using keyword groups:

* Joy
* Sadness
* Anger
* Fear
* Surprise
* Love

Useful for emotional support or personality-driven chatbots.

### ✅ **4. JSON Knowledge Base**

Stores question–answer pairs in a `knowledge_base.json` file.

Supports:

* Fuzzy matching
* Token overlap
* Normalized search
* Easy expansion by editing JSON

### ✅ **5. No External Dependencies**

Everything runs using **only Python standard libraries**:

* `json`
* `difflib`
* `re`
* `os`
* `collections`

This makes it lightweight and beginner-friendly.

---

## 📂 Project Structure

```
📁 chatbot-project/
│
├── chatbot_sentiment_kb.py        # Main chatbot code
├── knowledge_base.json            # JSON database for Q&A
└── README.md                      # Project documentation
```

---

## 💾 Installation

### 1. Clone or download the project

```bash
git clone https://github.com/yourusername/chatbot-sentiment-kb.git
cd chatbot-sentiment-kb
```

### 2. Ensure you have Python 3.8+ installed

Check with:

```bash
python --version
```

---

## ▶️ Running the Chatbot

In your terminal, run:

```bash
python chatbot_sentiment_kb.py
```

You’ll see:

```
ChatBuddy: Hi! I'm ChatBuddy (rule + sentiment + KB).
Type 'bye' to exit.
```

Now start chatting!

---

## 📘 Knowledge Base (JSON)

The chatbot loads answers from `knowledge_base.json`.

Example entry:

```json
{
  "question": "what is flask",
  "answer": "Flask is a lightweight Python web framework for building web apps."
}
```

You can expand the bot’s knowledge just by adding more objects to the JSON list.

---

## 🎯 Sample Interactions

```
You: hi
ChatBuddy: Hey! Ask me anything.

You: how to resize images?
ChatBuddy (KB): You can use Python Pillow. Use Image.open(), resize(), and save().
[Sentiment detected: neutral]

You: i'm feeling sad today
ChatBuddy: I'm sorry to hear that. Want to talk about it?
[Sentiment: negative]

You: thank you
ChatBuddy: Anytime!
```

---

## 🧩 How It Works (Conceptual Breakdown)

### **1. Intent Matching**

Regex patterns detect greetings, farewells, and common phrases.

### **2. Sentiment Detection**

Compares tokens against positive/negative lexicons.

### **3. Emotion Detection**

Checks user tokens against emotion keyword sets.

### **4. Knowledge Base Lookup**

Uses:

* Token overlap ratio
* Fuzzy matching with `difflib.get_close_matches()`

to find the best Q/A result.

### **5. Fallback Mechanism**

If:

* No intent matched
* No KB entry matched
  → bot uses small-talk fallback responses.

---

## 🛠 Future Enhancements

Want to take it further? Here are good upgrade ideas:

### 🔹 Add VADER sentiment analysis

Using NLTK for more accurate polarity scores.

### 🔹 Add Flask API

Expose chatbot as an HTTP endpoint.

### 🔹 Build a Web UI

HTML + JS chatbox that connects to your Flask endpoint.

### 🔹 Store conversation history

In SQLite or MongoDB.

### 🔹 Add speech support

Using `pyttsx3` or Web Speech API.

I can help you build any of these — just ask!

---
