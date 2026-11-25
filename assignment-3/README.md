# Assignment 3 – AI Student Knowledge Assistant

## Project Overview

The AI Student Knowledge Assistant is a browser-based document retrieval application built using Python and Streamlit.

It allows users to upload TXT and PDF documents and search for relevant information using natural-language questions.

The application extracts document text, divides it into searchable passages, and retrieves relevant passages using TF-IDF vectorization and cosine similarity.

**Note:** This project implements information retrieval. It does not use a generative LLM to create answers.

## Features

- Upload TXT and PDF documents.
- Extract text from supported documents.
- Split extracted content into sentence-level searchable chunks.
- Convert text into TF-IDF features.
- Retrieve relevant passages using cosine similarity.
- Display relevance scores for retrieved passages.
- Reject queries when no sufficiently relevant passage is found.
- Provide a simple browser-based interface using Streamlit.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | Web interface |
| scikit-learn | TF-IDF vectorization |
| Cosine similarity | Passage ranking |
| pypdf | PDF text extraction |

## How It Works

1. The user uploads a TXT or PDF document.
2. The application extracts readable text.
3. The extracted text is divided into sentence-level chunks.
4. TF-IDF converts the chunks into numerical feature vectors.
5. The user's question is converted using the same vectorizer.
6. Cosine similarity ranks passages according to lexical similarity.
7. The application displays the most relevant passages when their scores exceed the configured minimum.

## Run the Application

From the repository root, install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Start the application:

```bash
python -m streamlit run assignment-3/app.py --server.address 0.0.0.0
```

Open the forwarded port 8501 in GitHub Codespaces.

## Challenges and Learning

Building this project was challenging because I had to handle different document formats, extract their text, and split the content into meaningful chunks without losing context.

I also had to implement TF-IDF vectorization and cosine similarity to retrieve relevant passages instead of relying on simple keyword matching.

Another challenge was understanding the security requirements of document-based AI systems, including file validation, private-document access control, and prompt-injection risks.

## Current Limitations

- TF-IDF is based on lexical similarity and does not understand meaning as deeply as embedding-based semantic search.
- The application retrieves evidence passages but does not generate answers using an LLM.
- Retrieval quality depends on document content, chunking, and the relevance threshold.
- Authentication, document-level authorization, malware scanning, and production-grade file controls are not implemented in this prototype.

## Future Improvements

- Integrate an embedding model for semantic retrieval.
- Add a vector database such as ChromaDB.
- Connect an LLM to generate answers grounded in retrieved passages.
- Add authentication and document-level access control.
- Improve retrieval evaluation and document-processing reliability.