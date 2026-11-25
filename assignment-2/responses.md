# Assignment 2 – AI, LLMs, and Vector Databases

## 1. Self-assessment

These ratings reflect my current practical knowledge, project experience, and ability to implement concepts independently.

| Area | Rating | Basis |
|---|---|---|
| LLM | C | I understand basic use cases and high-level workflows of Large Language Models. I am currently learning how to build and integrate LLM-based applications independently. |
| Deep Learning | C | I have introductory exposure to neural-network concepts and face-recognition project components, but I am still developing my understanding of deep-learning model development. |
| AI | B | I understand common AI workflows and have implemented academic projects involving practical AI and machine-learning techniques. I may need guidance when working with unfamiliar AI systems. |
| ML | B | I have used TF-IDF and Logistic Regression in a fake news detection project. I am continuing to improve my knowledge of model selection, evaluation, and independent implementation. |

## 2. Key architectural components of an LLM-based chatbot

An LLM-based chatbot consists of multiple components that work together to receive user queries, process context, generate responses, and return useful information.

### Main architectural components

1. **User Interface:** Provides an interface through which users can enter questions and receive responses. It can be a web application, mobile application, or messaging interface.

2. **Backend/API Layer:** Receives user requests, validates inputs, handles authentication, applies rate limits, and coordinates communication between different components.

3. **Conversation Manager:** Maintains relevant conversation history and provides the necessary context for the current query. It also manages conversation length and token limits.

4. **Knowledge Retrieval (RAG):** Retrieves relevant information from external knowledge sources when the chatbot needs information that may not be available in the LLM's existing knowledge. Documents are processed, divided into chunks, converted into embeddings, and stored in a vector database.

5. **Prompt Construction:** Combines system instructions, the user's question, relevant conversation history, and retrieved information into a structured prompt for the LLM.

6. **LLM Inference:** Sends the prepared prompt to a hosted LLM API or a self-hosted model. The model processes the input and generates a response.

7. **Post-processing and Safety:** Validates the generated response, checks its format, applies safety rules, and handles sensitive information where required.

8. **Monitoring and Logging:** Tracks application performance, response time, errors, token usage, and relevant operational metrics. Sensitive information should be appropriately protected in logs.

### High-level architecture flow

```text
                  User
                    |
                    v
             Web / Mobile UI
                    |
                    v
                Backend API
                    |
          Authentication and
             Rate Limiting
                    |
                    v
          Conversation Manager
                    |
                    v
             Prompt Builder
                    |
          +---------+---------+
          |                   |
          v                   v
    User Question       RAG Pipeline
                              |
                              v
                       Vector Database
                              |
                              v
                       Relevant Context
                              |
          +-------------------+
          |
          v
        LLM Model
          |
          v
   Response Validation
          |
          v
         User
```

### Why use Retrieval-Augmented Generation (RAG)?

A general-purpose LLM may not have access to an organization's latest, private, or domain-specific information.

Retrieval-Augmented Generation (RAG) addresses this limitation by retrieving relevant information from an approved knowledge source and providing it as additional context to the LLM before generating a response.

For example, an internal company chatbot can retrieve relevant information from company policies, technical documentation, and support guides before answering an employee's question.

Benefits of RAG include:

- Provides access to external and updated information.
- Helps ground responses in relevant source documents.
- Reduces dependence on information learned during model training.
- Allows organizations to use their own knowledge sources.
- Makes it possible to identify the documents supporting an answer.

However, RAG does not guarantee correct answers. The quality of the response depends on document quality, retrieval accuracy, prompt construction, and the LLM itself.

### Security considerations

Security is important when developing LLM-based applications, particularly when processing private documents or user information.

- **Authentication and authorization:** Verify users and enforce document-level access control before retrieving information.
- **Secret management:** Store API keys and credentials securely using environment variables or a secret-management service.
- **Prompt injection protection:** Treat uploaded documents and retrieved content as untrusted data rather than system instructions.
- **Input validation:** Validate user inputs and uploaded files before processing them.
- **Output validation:** Check generated responses for unsafe content, sensitive information, and invalid output formats.
- **Rate limiting:** Limit excessive requests to protect application resources and external APIs.
- **Data privacy:** Avoid sending confidential information to external model providers without appropriate approval.
- **Monitoring:** Monitor errors, retrieval quality, access-control failures, and potential data leakage.

## 3. Vector databases

A vector database is a database designed to store, manage, and search numerical representations called **embeddings**.

An embedding model converts information such as text or images into numerical vectors. These vectors represent features of the original data and can be compared to identify semantically similar information.

Unlike traditional keyword-based searches, vector similarity search can retrieve related information even when the exact words in the query and document are different.

For example, a user searches for:

"How can I reset my password?"

A vector database may retrieve a document titled:

"Account recovery steps"

This is possible because the two pieces of text may have similar semantic representations.

### Typical vector database workflow

1. **Document collection:** Collect documents from approved knowledge sources.
2. **Text extraction:** Extract readable content from documents.
3. **Chunking:** Divide large documents into smaller, manageable sections.
4. **Embedding generation:** Convert each text chunk into a numerical vector using an embedding model.
5. **Vector storage:** Store embeddings along with their original text, identifiers, and metadata.
6. **Query embedding:** Convert the user's question into an embedding using the same compatible embedding model.
7. **Similarity search:** Compare the query vector with stored vectors using a similarity measure such as cosine similarity.
8. **Retrieval:** Return the most relevant document chunks.
9. **Access control:** Apply authorization and metadata filters before returning retrieved information.
10. **Application integration:** Pass the authorized retrieved context to the application or an LLM to generate a response.

### Hypothetical use case and vector database selection

**Problem statement:**

Consider a small organization's internal IT help desk. Employees frequently ask questions about password resets, software installation, network issues, and company IT policies.

The organization wants to build a chatbot that can search its approved troubleshooting guides and documentation to provide relevant information to employees.

**Selected vector database: ChromaDB**

For this small-scale prototype, I would choose ChromaDB.

Reasons for selecting ChromaDB:

- It provides a straightforward Python integration.
- It supports storing embeddings, documents, and metadata.
- It supports similarity search to retrieve relevant information.
- It supports metadata filtering.
- It is convenient for local development and proof-of-concept applications.

**Alternatives:**

Other options include:

- **Pinecone:** A managed vector database that can be considered for scalable applications.
- **Weaviate:** A vector database supporting vector search and additional data-management capabilities.
- **PostgreSQL with pgvector:** An extension that enables vector similarity search within PostgreSQL.

For a production implementation, I would evaluate these alternatives based on expected data volume, search latency, scalability, access-control requirements, hosting, maintenance, and overall cost.

### Limitations of vector databases

- Vector similarity does not guarantee factual correctness.
- Poor document chunking can reduce retrieval quality.
- The quality of embeddings affects search results.
- Similarity search may retrieve irrelevant information.
- Sensitive information requires appropriate authorization and filtering.
- Large-scale systems may require additional optimization and infrastructure.

Techniques such as hybrid search, reranking, metadata filtering, and retrieval evaluation can help improve search quality and reliability.

## Conclusion

LLMs, Retrieval-Augmented Generation, and vector databases can work together to build applications that provide information from external knowledge sources.

A well-designed chatbot should combine an appropriate backend architecture, reliable retrieval, secure data handling, and response validation. The choice of technologies should depend on the application's requirements, expected scale, security needs, and operational constraints.