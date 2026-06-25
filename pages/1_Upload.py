import streamlit as st #for creating the web page
from backend.pdf_reader import extract_text_from_pdf
from backend.chunking import create_chunks
from backend.embeddings import get_embedding
from backend.vectordb import store_chunks
import os
st.set_page_config(page_title="Upload PDF", layout="wide")#page title and layout
st.title("📚 Upload Course Material")#uploading pdf material
uploaded_file = st.file_uploader(#file uploader for pdf
    "Upload your PDF file",
    type=["pdf"]
)
if uploaded_file is not None:#
    save_path = os.path.join("uploaded_files", uploaded_file.name)#now saving this uploaded file to the  folder uploaded-files
    with open(save_path, "wb") as f:#savinf file in folder
        f.write(uploaded_file.getbuffer())
    st.success(f"{uploaded_file.name} uploaded successfully!")#after uplaading successfully shows this
    extracted_text = extract_text_from_pdf(save_path) #extracting text from the uploaded pdf file
    st.subheader("Extracted Text")
    st.write(extracted_text[:1000])
    chunks = create_chunks(extracted_text) # creating chunks from the extracted text
    st.subheader("Text Chunks") #displaying the created chunks
    st.write(f"Total Chunks Created: {len(chunks)}") #displaying the total number of chunks created
    embeddings = [] #empty list for stroing the embedding vectors for each chunk
    for chunk in chunks:
        embedding = get_embedding(chunk)
        embeddings.append(embedding)
    store_chunks(chunks, embeddings)
    st.success("Embeddings stored in ChromaDB successfully!")
    for i, chunk in enumerate(chunks):
        st.markdown(f"### Chunk {i+1}")
        st.write(chunk)
        st.divider()