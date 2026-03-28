# System Architecture - Smart Q&A RAG Pipeline

## 🏗️ High-Level Architecture

```mermaid
graph TB
    A[User Question] --> B[Main Entry Point]
    B --> C[Crew AI Pipeline]
    
    C --> D[Phase 1: Document Processing]
    D --> D1[Load PDF/TXT]
    D1 --> D2[Split into Chunks]
    D2 --> D3[Create Embeddings]
    D3 --> D4[Store in ChromaDB]
    
    C --> E[Phase 2: Question Answering]
    E --> E1[Agent 1: Document Retriever]
    E1 --> E2[RAG Search Tool]
    E2 --> E3[Query ChromaDB]
    E3 --> E4[Retrieve Top 3 Chunks]
    
    E4 --> F[Agent 2: Answer Writer]
    F --> G[Gemini LLM + Memory]
    G --> H[Synthesize Answer]
    
    H --> I[Agent 3: Quality Checker]
    I --> J[Compare with Sources]
    J --> K[Calculate Confidence]
    K --> L[Final Output]
    
    L --> M[Answer + Sources + Confidence]
```

## 🔄 Sequential Agent Workflow

```mermaid
graph LR
    A[User Question] --> B[Task 1: Document Retrieval]
    B --> C{Context Injection}
    C --> D[Task 2: Answer Writing]
    D --> E{Context Injection}
    E --> F[Task 3: Quality Checking]
    F --> G[Final Result]
```

## 📦 Component Breakdown

### Phase 1: Document Processing Pipeline

```mermaid
graph LR
    A[docs/ folder] --> B[PDF/TXT Files]
    B --> C[RAGSetup.py]
    C --> D[PyPDF2/TextLoader]
    D --> E[Raw Documents]
    E --> F[RecursiveCharacterTextSplitter]
    F --> G[Document Chunks]
    G --> H[HuggingFace Embeddings]
    H --> I[Vector Representations]
    I --> J[ChromaDB Storage]
```

### Phase 2: Query Processing Pipeline

```mermaid
graph TB
    A[User Question] --> B[Main.py]
    B --> C[Crew.py]
    C --> D{CrewAI Sequential Process}
    
    D --> E[Agent 1: Document Retriever]
    E --> F[RAG Search Tool]
    F --> G[ChromaDB Query]
    G --> H[Similarity Search]
    H --> I[Top 3 Chunks + Scores]
    
    I --> J[Agent 2: Answer Writer]
    J --> K[Context from Agent 1]
    K --> L[Gemini Pro LLM]
    L --> M[CrewAI Memory]
    M --> N[Draft Answer]
    
    N --> O[Agent 3: Quality Checker]
    O --> P[Original Chunks]
    P --> Q[Source Comparison]
    Q --> R[Factual Verification]
    R --> S[Confidence Score]
    S --> T[Final Answer with Sources]
```

## 🔧 Detailed Component Interactions

```mermaid
graph TB
    subgraph "Environment Setup"
        A1[.env file] --> A2[GOOGLE_API_KEY]
        A2 --> A3[ChatGoogleGenerativeAI]
    end
    
    subgraph "Document Layer"
        B1[docs/*.pdf] --> B2[PyPDFLoader]
        B3[docs/*.txt] --> B4[TextLoader]
        B2 --> B5[Documents]
        B4 --> B5
        B5 --> B6[TextSplitter]
        B6 --> B7[Chunks]
        B7 --> B8[Embeddings]
        B8 --> B9[(ChromaDB)]
    end
    
    subgraph "Agent Layer"
        C1[Document Retriever] --> C2[RAGSearchTool]
        C2 --> C3[ChromaDB Query]
        
        C4[Answer Writer] --> C5[Gemini LLM]
        C5 --> C6[CrewAI Memory]
        
        C7[Quality Checker] --> C8[Source Comparison]
        C8 --> C9[Confidence Calculation]
    end
    
    subgraph "Task Layer"
        D1[Retrieval Task] --> D2[Search & Return Chunks]
        D3[Writing Task] --> D4[Synthesize Answer]
        D5[Quality Task] --> D6[Verify & Score]
    end
    
    A3 --> C5
    B9 --> C3
    C3 --> D1
    D1 --> D2
    D2 --> D3
    D3 --> D4
    D4 --> D5
    D5 --> D6
```

## 🎯 Data Flow Diagram

```mermaid
graph LR
    A[Input Documents] --> B[Vector Store]
    B --> C[Retrieved Chunks]
    C --> D[Generated Answer]
    D --> E[Verified Answer]
    E --> F[User Output]
    
    G[User Question] --> H[Query Vector]
    H --> B
    I[API Key] --> J[LLM Processing]
    J --> D
    K[Source Docs] --> L[Verification]
    L --> E
```

## 📊 File Dependencies

```mermaid
graph TB
    A[main.py] --> B[crew.py]
    A --> C[.env]
    
    B --> D[agents.py]
    B --> E[tasks.py]
    
    D --> F[rag_tool.py]
    D --> G[langchain_google_genai]
    
    E --> D
    
    F --> H[chromadb]
    F --> I[sentence-transformers]
    
    J[rag_setup.py] --> H
    J --> I
    J --> K[PyPDF2]
    J --> L[TextLoader]
```

## 🏛️ System Layers

### Layer 1: Infrastructure
- **ChromaDB**: Vector database for semantic search
- **HuggingFace**: Embedding model (all-MiniLM-L6-v2)
- **Google Gemini**: LLM for text generation

### Layer 2: Data Processing
- **RAGSetup.py**: Document loading and preprocessing
- **TextSplitter**: Chunk creation with overlap
- **Embeddings**: Semantic vector representations

### Layer 3: Agent Framework
- **CrewAI**: Multi-agent orchestration
- **Custom Tools**: RAG search integration
- **Memory**: Context retention across tasks

### Layer 4: Application Logic
- **Sequential Process**: Ordered task execution
- **Context Injection**: Passing results between agents
- **Quality Assurance**: Verification and scoring

### Layer 5: User Interface
- **CLI Interface**: Interactive question-answer loop
- **Formatted Output**: Structured results display
- **Error Handling**: User-friendly messages

## 🔐 Security Architecture

```mermaid
graph TB
    A[User Input] --> B[Input Validation]
    B --> C[Local Processing]
    C --> D[API Call]
    
    D --> E[HTTPS Secure Connection]
    E --> F[Google Gemini API]
    F --> G[Response]
    
    H[.env file] --> I[API Key]
    I --> D
    
    J[Local Vector Store] --> K[No External Storage]
    C --> K
```

## 📈 Performance Considerations

### Memory Usage
- Embeddings loaded once at startup
- ChromaDB persists to disk
- CrewAI memory enables context without re-computation

### Speed Optimizations
- Chunk caching avoids re-processing
- Vector store persistence
- Sequential processing prevents race conditions

### Scalability
- Add more documents → Automatic chunk indexing
- Multiple questions → CrewAI memory maintains context
- Larger documents → Configurable chunk parameters

---

This architecture ensures:
✅ **Accuracy**: Source-grounded responses  
✅ **Transparency**: Clear source attribution  
✅ **Reliability**: Quality verification at each step  
✅ **Scalability**: Easy to add more documents  
✅ **Maintainability**: Modular component design
