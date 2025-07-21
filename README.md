# 📚 Query-Stream


Upload any text or PDF file and ask questions about it — get accurate, AI-generated answers using Retrieval-Augmented Generation (RAG) with **local models** via Ollama.

No cloud, no API keys — 100% private and local.

---

## 🧠 What is this?

A private AI assistant for your documents!

- Upload a document (TXT or PDF)
- App splits and indexes it into a vector store using `ChromaDB`
- When you ask a question, it retrieves relevant chunks using semantic similarity
- Passes those chunks as context to a local LLM via Ollama (like `llama3.2:3b`)
- You get precise answers from **your own data** — privately and offline!

---

## 🖼️ UI Preview

<img width="1920" height="815" alt="Screenshot 2025-07-21 165510" src="https://github.com/user-attachments/assets/5634e03d-7516-4d83-9ad9-d85180dfe82f" />


<img width="1893" height="832" alt="Screenshot 2025-07-21 165536" src="https://github.com/user-attachments/assets/db7d007a-7daf-4373-bba1-89d65aa60faf" />


## 🧰 Tech Stack

| 🛠️ Tool      | 🔧 Role                              |
|--------------|--------------------------------------|
| Python       | Core backend                         |
| Streamlit    | Frontend interface                   |
| LangChain    | Document splitting & retrieval       |
| ChromaDB     | Vector database                      |
| Ollama       | Local LLM & embeddings               |
| llama3.2:3b  | Default local model (can be changed) |

---

## ✨ Features

- 📄 Upload PDFs or TXT files  
- 🔍 Ask questions and get relevant, contextual answers  
- 🧠 RAG-based workflow using local embeddings & models  
- 🎨 Colorful UI with purple and blue palette  
- 📤 Export answers as `.txt` file  
- 🔒 100% private & runs fully offline

---

## ⚙️ How to Run Locally

### 1️⃣ Prerequisites

- Python 3.10+
- Git
- Ollama installed → https://ollama.com/download
- Model pulled locally → `ollama pull llama3.2:3b`

### 2️⃣ Clone the Repo

```bash
git clone https://github.com/Pushpachoudary/Query-Stream.git
cd Query-Stream
```

### 3️⃣ (Optional) Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate     # On Windows
source venv/bin/activate  # On Mac/Linux
```

### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 5️⃣ Run the App

```bash
streamlit run app.py
```

> Make sure Ollama is running in the background and the model (like `llama3.2:3b`) is pulled.

---

## 📤 Export Feature

After getting answers, use the **"Export Answer"** button to save the response to a `.txt` file locally.

---

## 📁 Folder Structure

```bash
Query-Stream/
│
├── app.py                # Main Streamlit app
├── requirements.txt      # Python dependencies
├── README.md             # Project info
└── .venv/                # (optional) virtual environment
```

---

## 📌 Notes

- You can change the model from llama3.2:3b to any Ollama-supported LLM
- Supports only single document at a time (multi-doc feature coming soon)
- All data and models stay on your device — no uploads or APIs

---

## 👨‍💻 Author

**Pushpa Choudary**  
B.Tech CSE (AI & ML) Graduate  
[GitHub Profile »](https://github.com/Pushpachoudary)

---

## ⭐️ Show your support

If you find this project helpful, consider giving it a ⭐ and sharing with others!

---
