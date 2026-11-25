
"""Document Q&A prototype using sentence-level TF-IDF retrieval."""

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


def split_into_chunks(text):
    # Split the document into individual sentences.
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())

    # Remove empty sentences and very short fragments.
    chunks = [
        sentence.strip()
        for sentence in sentences
        if len(sentence.strip().split()) >= 3
    ]

    return chunks


def retrieve(question, chunks, top_k=3, min_score=0.0):
    if not question.strip() or not chunks:
        return []

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        sublinear_tf=True
    )

    matrix = vectorizer.fit_transform(chunks + [question])

    scores = cosine_similarity(
        matrix[-1],
        matrix[:-1]
    ).flatten()

    ranked_indices = scores.argsort()[::-1]

    results = []

    for index in ranked_indices:
        score = float(scores[index])

        if score <= min_score:
            continue

        results.append((chunks[index], score))

        if len(results) >= top_k:
            break

    return results


st.set_page_config(
    page_title="Student Knowledge Assistant",
    page_icon="📚"
)

st.title("Student Knowledge Assistant")

st.caption(
    "A document-retrieval prototype using sentence-level TF-IDF. "
    "It does not generate LLM answers."
)

uploaded = st.file_uploader(
    "Upload a TXT or PDF document",
    type=["txt", "pdf"]
)

if uploaded:
    try:
        document_text = extract_text(uploaded)

        chunks = split_into_chunks(document_text)

        if not chunks:
            st.warning("No readable text was found in this document.")

        else:
            st.success(
                f"Extracted text and created {len(chunks)} searchable chunks."
            )

            question = st.text_input(
                "Ask a question about your document"
            )

            if st.button("Search document", type="primary"):
                if not question.strip():
                    st.warning("Please enter a question.")

                else:
                    results = retrieve(question, chunks)

                    if not results:
                        st.warning(
                            "No sufficiently relevant passage was found. "
                            "Try asking a question using terms from the document."
                        )

                    else:
                        st.subheader("Retrieved evidence")

                        for number, (chunk, score) in enumerate(
                            results, start=1
                        ):
                            with st.expander(
                                f"Result {number} · similarity {score:.3f}",
                                expanded=True
                            ):
                                st.write(chunk)

                        st.info(
                            "These are retrieved source passages, "
                            "not verified generated answers."
                        )

    except Exception as error:
        st.error(f"Could not process this document: {error}")

else:
    st.info(
        "Upload a TXT or PDF file to begin. "
        "Sample documents are available in the repository."
    )
