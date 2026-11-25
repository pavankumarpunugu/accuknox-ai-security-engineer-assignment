# Assignment 3 – AI Student Knowledge Assistant

## Project overview
A browser-based document assistant prototype. A user uploads a TXT or PDF document,
asks a question, and the application retrieves the most relevant text passages using
TF-IDF similarity.

## Why this project is challenging
1. Documents have different formats and structures, so text extraction and chunking must
   preserve enough context for useful retrieval.
2. A search result can be textually similar but still irrelevant; retrieval quality needs
   evaluation and careful chunk sizing.
3. A real deployment must protect private documents with authentication, access control,
   upload validation, secure storage, and prompt-injection defenses.

## Architecture

```text
Document upload (TXT/PDF)
        |
        v
Text extraction
        |
        v
Chunking
        |
        v
TF-IDF vectorization and indexing
        |
        v
User question -> query vector
        |
        v
Similarity ranking
        |
        v
Relevant evidence snippets + source labels
```

## Important scope statement
This is a retrieval-based prototype, not a full generative LLM chatbot. It returns evidence
snippets from the uploaded material and does not pretend that a language model generated
a synthesized answer. An approved LLM API can be added later with secure secret management.
