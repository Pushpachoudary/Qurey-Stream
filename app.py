import os
import tempfile

import chromadb
import ollama
import streamlit as st
from chromadb.utils.embedding_functions.ollama_embedding_function import OllamaEmbeddingFunction
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import CrossEncoder
from streamlit.runtime.uploaded_file_manager import UploadedFile

# System prompt
system_prompt = """
You are an AI assistant tasked with providing detailed answers based solely on the given context...
"""

# 🧠 Vector DB Setup
def get_vector_collection():
    client = chromadb.Client()
    embedding_function = OllamaEmbeddingFunction(model_name="llama3.2:3b")
    return client.get_or_create_collection(
        name="rag_documents",
        embedding_function=embedding_function,
    )

# 📄 PDF Processing
def process_document(uploaded_file: UploadedFile) -> list[Document]:
    with tempfile.NamedTemporaryFile("wb", suffix=".pdf", delete=False) as temp_file:
        temp_file.write(uploaded_file.read())
        temp_path = temp_file.name

    try:
        loader = PyMuPDFLoader(temp_path)
        docs = loader.load()
    finally:
        os.unlink(temp_path)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", "?", "!", " ", ""],
    )
    return splitter.split_documents(docs)

# 📥 Add Chunks to Vector DB
def add_to_vector_collection(splits: list[Document], file_name: str):
    collection = get_vector_collection()
    documents, metadatas, ids = [], [], []

    for idx, split in enumerate(splits):
        documents.append(split.page_content)
        metadatas.append(split.metadata)
        ids.append(f"{file_name}_{idx}")

    collection.upsert(
        documents=documents,
        metadatas=metadatas,
        ids=ids,
    )
    st.success("✅ Data added to vector store!")

# 🔍 Query
def query_collection(prompt: str, n_results: int = 10):
    collection = get_vector_collection()
    results = collection.query(query_texts=[prompt], n_results=n_results)
    return results

# 🧠 Re-Ranking
def re_rank_cross_encoders(docs: list[str], prompt: str) -> tuple[str, list[int]]:
    if not docs:
        raise ValueError("No documents to re-rank.")
    encoder_model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    ranks = encoder_model.rank(prompt, docs, top_k=3)

    relevant_text = ""
    top_ids = []
    for rank in ranks:
        relevant_text += docs[rank["corpus_id"]] + "\n\n"
        top_ids.append(rank["corpus_id"])

    return relevant_text, top_ids

# 🧠 Call Ollama Model
def call_llm(context: str, prompt: str):
    response = ollama.chat(
        model="llama3.2:3b",
        stream=True,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Context: {context}\nQuestion: {prompt}"},
        ],
    )
    for chunk in response:
        if not chunk["done"]:
            yield chunk["message"]["content"]
        else:
            break

# 🎨 Streamlit UI
st.set_page_config(page_title="📘 RAG QnA", layout="wide")

# 💅 Custom CSS
st.markdown("""
    <style>
    body {
        background-color: #f3f0ff;
        color: #2d1b6d;
    }
    .stButton>button {
        background-color: #6a5acd;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 8px 20px;
    }
    .stTextArea textarea {
        background-color: #ffffff;
        color: #1a0033;
        border-radius: 10px;
        font-weight: 500;
    }
    .stMarkdown h1, h2 {
        color: #4b0082;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📘 RAG-Powered Document QA")

# 📎 Sidebar Upload
with st.sidebar:
    st.header("📥 Upload PDF")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
    process = st.button("⚡ Process PDF")

# 🧩 Process File
if uploaded_file and process:
    normalized_name = uploaded_file.name.translate(str.maketrans({"-": "", ".": "", " ": "_"}))
    splits = process_document(uploaded_file)
    add_to_vector_collection(splits, normalized_name)

# 🗣 Ask
st.header("💬 Ask a Question About Your Document")
prompt = st.text_area("Type your question here", height=100, placeholder="e.g., What is the main topic in the document?")
ask = st.button("🔍 Ask Question")

if ask and prompt:
    results = query_collection(prompt)
    docs = results.get("documents", [[]])[0]

    if not docs:
        st.warning("❌ No relevant information found in document.")
    else:
        relevant_text, relevant_ids = re_rank_cross_encoders(docs, prompt)
        response_gen = call_llm(context=relevant_text, prompt=prompt)

        # 📤 Answer Export
        st.subheader("🧠 Answer")
        full_answer = st.write_stream(response_gen)

        st.download_button(
            label="⬇️ Export Answer",
            data=full_answer,
            file_name="answer.txt",
            mime="text/plain",
        )

        with st.expander("📑 Retrieved Document Info"):
            st.caption("🔹 You usually don’t need to see this unless debugging.")
            st.json(results)
