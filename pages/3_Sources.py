import streamlit as st

st.set_page_config(page_title="Sources", layout="wide")

st.title(" Knowledge Base Dashboard")

# Metrics Section
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(" Documents", "1")

with col2:
    st.metric(" Chunks Indexed", "42")

with col3:
    st.metric(" Retriever Top-K", "3")

st.divider()

# System Information
st.subheader("System Configuration")

col1, col2 = st.columns(2)

with col1:
    st.info("""
     Vector Database: ChromaDB

     Embedding Model: all-MiniLM-L6-v2

     Retrieval Method: Semantic Similarity Search
    """)

with col2:
    st.info("""
     LLM: OpenRouter GPT-3.5 Turbo

     Quiz Generation: Context-Aware MCQs

     Memory: Session State Memory
    """)

st.divider()

# Active Document Section
st.subheader(" Active Document")

st.success("""
Document Loaded Successfully

Status: Ready for Retrieval & Question Answering
""")

st.divider()

# Architecture Section
st.subheader(" RAG Architecture")

st.code("""
PDF Upload
     ↓
Text Extraction
     ↓
Chunking
     ↓
Embeddings
     ↓
ChromaDB
     ↓
Retriever
     ↓
LLM
     ↓
Answer Generation
     ↓
Quiz Generation
""")

st.divider()

# Status Section
st.subheader(" System Status")

st.success("Knowledge Base Ready")