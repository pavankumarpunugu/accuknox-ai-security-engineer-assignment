"""Document Q&A prototype using TF-IDF retrieval (not generative LLM output)."""
import io
import re

import streamlit as st
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def extract_text(uploaded_file):
    name = uploaded_file.name.lower()
    raw = uploaded_file.getvalue()

    if name.endswith(".txt"):
        return raw.decode("utf-8", errors="replace")
    if name.endswith(".pdf"):
        reader = PdfReader(io.BytesIO(raw))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    raise ValueError("Please upload a TXT or PDF file.")


def split_into_chunks(text, max_words=110, overlap=20):
    words = re.findall(r"\S+", text)
    if not words:
        return []
    chunks = []
    step = max(1, max_words - overlap)
    for start in range(0, len(words), step):
        chunk = " ".join(words[start:start + max_words])
        if chunk:
            chunks.append(chunk)
        if start + max_words >= len(words):
            break
    return chunks


def retrieve(question, chunks, top_k=3):
    if not question.strip() or not chunks:
        return []
    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(chunks + [question])
    scores = cosine_similarity(matrix[-1], matrix[:-1]).flatten()
    ranked = scores.argsort()[::-1][:top_k]
    return [(chunks[index], float(scores[index])) for index in ranked if scores[index] > 0]


st.set_page_config(page_title="Student Knowledge Assistant", page_icon="📚")
st.title("Student Knowledge Assistant")
st.caption("A small document-retrieval prototype using TF-IDF. It does not generate LLM answers.")

uploaded = st.file_uploader("Upload a TXT or PDF document", type=["txt", "pdf"])

if uploaded:
    try:
        document_text = extract_text(uploaded)
        chunks = split_into_chunks(document_text)
        st.success(f"Extracted text and created {len(chunks)} searchable chunks.")
        question = st.text_input("Ask a question about your document")

        if st.button("Search document", type="primary"):
            results = retrieve(question, chunks)
            if not results:
                st.warning("No relevant text was found. Try rephrasing your question.")
            else:
                st.subheader("Retrieved evidence")
                for number, (chunk, score) in enumerate(results, start=1):
                    with st.expander(f"Result {number} · similarity {score:.3f}", expanded=True):
                        st.write(chunk)
                st.info("These are retrieved source passages, not a verified generated answer.")
    except Exception as error:
        st.error(f"Could not process this document: {error}")
else:
    st.info("Upload a TXT or PDF file to begin. A sample document is available in the repository.")
