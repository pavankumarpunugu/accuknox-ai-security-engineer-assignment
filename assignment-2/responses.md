# Assignment 2 – AI, LLMs, and Vector Databases

## 1. Self-assessment

The following is a conservative draft and must be adjusted to match what I can genuinely
implement without help.

| Area | Suggested rating | Basis |
|---|---|---|
| LLM | C | I understand the basic use cases and high-level workflow, but I am still learning to build LLM applications independently. |
| Deep Learning | C | I have introductory exposure to neural-network concepts and face-recognition project components, but cannot claim independent deep-learning model development expertise. |
| AI | B | I understand common AI workflows and have implemented academic projects involving practical AI/ML techniques, while still needing guidance for unfamiliar systems. |
| ML | B | I have used techniques such as TF-IDF and Logistic Regression in a project context; I am continuing to strengthen model selection, evaluation, and independent implementation. |

**Assumption:** These ratings describe current practical ability, not theoretical familiarity alone. Change any rating if it does not accurately describe your ability.

## 2. Key architectural components of an LLM-based chatbot

A typical LLM chatbot can be designed as the following pipeline:

1. **User interface:** Accepts a question and displays the answer. It may be a web application, mobile application, or messaging interface.
2. **Backend/API layer:** Receives requests, validates inputs, authenticates users, applies rate limits, and coordinates the workflow.
3. **Conversation manager:** Maintains relevant conversation history and constructs the context for the current request. It should enforce token and retention limits.
4. **Knowledge retrieval (optional RAG):** Searches trusted documents for relevant passages. Documents are cleaned, split into chunks, converted into embeddings, and indexed in a vector store.
5. **Prompt construction:** Combines system instructions, the user question, relevant retrieved passages, and limited conversation context. Retrieved content must be treated as data, not trusted instructions.
6. **LLM inference:** Sends the prompt to a hosted model API or an internally deployed model and receives generated text.
7. **Post-processing and safety:** Checks output format, removes or masks sensitive information where required, applies policy checks, and avoids unsupported claims.
8. **Observability:** Records operational metrics, latency, errors, token usage, and appropriately redacted audit events.

### High-level flow

```text
User
  |
  v
Web / Mobile UI
  |
  v
Backend API ---- Authentication / Rate limiting
  |
  v
Conversation manager
  |
  +----> Retrieval pipeline ----> Vector database
  |             |
  |             v
  |        Relevant passages
  |
  v
Prompt builder
  |
  v
LLM
  |
  v
Safety checks / response validation
  |
  v
User
```

### Why use RAG?

A general LLM may not know an organization's latest or private documents. Retrieval-Augmented Generation (RAG) first retrieves relevant material from an approved knowledge source and then provides that material as context to the LLM. This can improve grounding and make answers easier to trace to source documents. RAG does not guarantee correctness; retrieval quality, source quality, prompt design, and evaluation still matter.

### Security considerations

- Authenticate users and enforce document-level access control before retrieval.
- Do not place API keys or secrets in source code.
- Treat uploaded documents and retrieved text as untrusted input.
- Defend against prompt injection by separating instructions from retrieved content.
- Apply input validation, output checks, rate limits, and audit logging.
- Avoid sending confidential data to external model providers unless approved.
- Evaluate hallucinations, retrieval precision, access-control failures, and data leakage.

## 3. Vector databases

A vector database stores and searches numerical representations called **embeddings**. An embedding model converts text, images, or other data into vectors so that semantically related items can be found even when they do not share exact keywords.

For example, a search for “how do I reset my password?” may retrieve a document titled “Account recovery steps” because their embeddings are semantically similar.

### Typical workflow

1. Collect documents from approved sources.
2. Clean and split documents into manageable chunks.
3. Generate an embedding for each chunk.
4. Store each vector with its text, identifier, and metadata.
5. Embed the user's query.
6. Run similarity search (for example cosine similarity) to retrieve the closest chunks.
7. Apply metadata filters and access-control checks.
8. Pass authorized retrieved context to the application or LLM.

### Hypothetical use case and selection

**Problem:** A small internal IT help desk wants employees to search a collection of approved troubleshooting guides and policy documents.

**Choice: ChromaDB for a prototype.**

Reasons:
- It is straightforward to use from Python.
- It supports storing embeddings, documents, and metadata.
- It supports similarity search and metadata filtering.
- It is convenient for a small proof of concept and local development.

For a production system, I would benchmark ChromaDB against managed or distributed alternatives such as Pinecone, Weaviate, and PostgreSQL with pgvector. The decision should consider scale, latency, filtering, access control, operational requirements, hosting constraints, and total cost—not popularity alone.

### Limitations

Vector similarity is not the same as factual correctness. Poor chunking or embeddings can retrieve irrelevant content. Sensitive data must be filtered by authorization before it is returned. Hybrid search (keyword plus vector search), reranking, and evaluation datasets may improve retrieval quality.
