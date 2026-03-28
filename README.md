# Smart Q&A RAG Pipeline

A powerful Question-Answering system powered by CrewAI and Retrieval-Augmented Generation (RAG). This system can read PDF and TXT documents, understand their content, and provide accurate answers with source verification and confidence scores.

## 🚀 Features

- **Multi-Agent System**: 3 specialized agents working in sequence
  - Document Retriever: Searches ChromaDB for relevant information
  - Answer Writer: Synthesizes comprehensive answers using Gemini LLM
  - Quality Checker: Verifies answers and provides confidence scores

- **RAG Pipeline**: 
  - Splits documents into chunks (1000 tokens with 200 overlap)
  - Creates embeddings using sentence-transformers
  - Stores in ChromaDB vector store
  - Context injection between tasks

- **Source Verification**: Every answer includes highlighted source paragraphs
- **Confidence Scoring**: Quality assessment with factual accuracy checks
- **Memory Enabled**: Agents remember previous context through CrewAI memory

## 📁 Project Structure

```
Smart Q&A/
├── docs/                  # Drop your PDF or TXT files here
├── chroma_db/            # Vector store (created after running rag_setup.py)
├── chunk_cache/          # Cached document chunks
├── rag_setup.py          # Document loading and vector store creation
├── rag_tool.py           # Custom CrewAI tool for ChromaDB queries
├── agents.py             # Agent definitions (3 agents)
├── tasks.py              # Task definitions (3 tasks)
├── crew.py               # Crew assembly and execution
├── main.py               # Main entry point - user questions
├── SmartQ&A.py          # Alternative entry point
├── requirements.txt      # Python dependencies
└── .env                  # Environment variables (API keys)
```

## 🛠️ Setup Instructions

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Configure API Key

1. Get your Google Gemini API key from: https://makersuite.google.com/app/apikey
2. Create a `.env` file in the project root
3. Add your API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

### Step 3: Add Documents

Place your PDF or TXT files in the `docs/` folder.

### Step 4: Build Vector Store

Run the setup script to process documents:

```bash
python rag_setup.py
```

This will:
- Load all documents from `docs/`
- Split them into chunks
- Create embeddings
- Store in ChromaDB

### Step 5: Start Asking Questions!

Run the main application:

```bash
python main.py
```

Or use the alternative entry point:

```bash
python SmartQ&A.py
```

## 🎯 How It Works

### Phase 1: Document Processing
1. Documents are loaded from `docs/` folder
2. Split into chunks using RecursiveCharacterTextSplitter
3. Converted to embeddings using sentence-transformers
4. Stored in ChromaDB vector store

### Phase 2: Question Answering (Sequential Process)
1. **User types a question**
2. **Agent 1 - Document Retriever**: 
   - Uses RAG Search Tool to query ChromaDB
   - Retrieves top 3 most relevant chunks
3. **Agent 2 - Answer Writer**:
   - Receives retrieved chunks via context injection
   - Writes comprehensive answer using Gemini LLM
   - Uses CrewAI memory for context retention
4. **Agent 3 - Quality Checker**:
   - Verifies answer against original chunks
   - Provides confidence score (0-100%)
   - Highlights source paragraphs

## 📊 Output Format

The final answer includes:

1. **Confidence Score**: Overall confidence percentage
2. **Quality Assessment**: 
   - Factual Accuracy ✓/✗
   - Completeness ✓/✗
   - Source Support ✓/✗
   - No Hallucination ✓/✗
3. **Source Verification**: Which chunks support which parts
4. **Final Answer**: With highlighted source paragraphs

## 🔧 Configuration

### Chunk Settings (in rag_setup.py)
```python
chunk_size=1000      # Characters per chunk
chunk_overlap=200    # Overlap between chunks
```

### Embedding Model
- Using: `sentence-transformers/all-MiniLM-L6-v2`
- Can be changed in `rag_setup.py` and `rag_tool.py`

### LLM Model
- Using: Google Gemini Pro
- Configured in `agents.py`
- Temperature: 0.7

## 🐛 Troubleshooting

**No documents found**
- Make sure you have PDF/TXT files in the `docs/` folder
- Run `python rag_setup.py` to build the vector store

**GOOGLE_API_KEY not found**
- Create a `.env` file with your API key
- Check `.env.example` for format

**Vector store not available**
- Run `python rag_setup.py` first
- Check that `chroma_db/` folder exists

**Dependencies error**
- Run: `pip install -r requirements.txt`
- Upgrade pip if needed: `python -m pip install --upgrade pip`

## 📝 Example Usage

```
🤔 Your Question: What is machine learning?

⏳ Processing your question...

Agent Workflow:
  [1/3] Document Retriever → Searching ChromaDB...
  [2/3] Answer Writer → Synthesizing answer...
  [3/3] Quality Checker → Verifying and scoring...

================================================================================
                         FINAL ANSWER
================================================================================

CONFIDENCE SCORE: 95%

QUALITY ASSESSMENT:
  - Factual Accuracy: ✓
  - Completeness: ✓
  - Source Support: ✓
  - No Hallucination: ✓

SOURCE VERIFICATION:
  Supported by: document.pdf (Page 2), notes.txt

FINAL ANSWER WITH HIGHLIGHTED SOURCES:
[Your answer with highlighted source paragraphs...]
================================================================================
```

## 🔐 Privacy & Security

- All processing happens locally
- Documents are stored only on your machine
- API calls use secure HTTPS connections
- Never commit your `.env` file to version control

## 📄 License

This project is provided as-is for educational and research purposes.

## 🤝 Contributing

Feel free to customize the agents, tasks, and pipeline configuration to suit your needs!

---

**Made with ❤️ using CrewAI + RAG**
