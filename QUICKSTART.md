# Quick Start Guide - Smart Q&A RAG Pipeline

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies (2 minutes)
```bash
pip install -r requirements.txt
```

This installs:
- crewai & crewai-tools (Agent framework)
- langchain & langchain-community (LLM utilities)
- chromadb (Vector database)
- sentence-transformers (Embeddings)
- PyPDF2 (PDF processing)
- google-generativeai (Gemini LLM)
- python-dotenv (Environment variables)

### Step 2: Set Your API Key (1 minute)

**Option A: Create .env file**
```bash
# Copy the example file
copy .env.example .env

# Edit .env and add your API key
notepad .env
```

Add this line (replace with your actual key):
```
GOOGLE_API_KEY=AIzaSy...your_actual_key_here
```

**Option B: Set environment variable directly**
```bash
# Windows PowerShell
$env:GOOGLE_API_KEY="your_api_key_here"

# Windows CMD
set GOOGLE_API_KEY=your_api_key_here
```

**Get your API key:**
1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key

### Step 3: Build Vector Store (1 minute)

The sample document is already in `docs/` folder. Just run:

```bash
python rag_setup.py
```

You should see:
```
============================================================
RAG SETUP PIPELINE
============================================================
Loading TXT: sample_ml_basics.txt

Total documents loaded: 1

Splitting documents into chunks...
Total chunks created: 2

Creating ChromaDB vector store...
Vector store created successfully!

============================================================
RAG SETUP COMPLETED SUCCESSFULLY!
============================================================
```

### Step 4: Ask Your First Question! (1 minute)

```bash
python main.py
```

Try these sample questions:
- "What is machine learning?"
- "What are the types of machine learning?"
- "Explain supervised vs unsupervised learning"
- "What is overfitting?"

## 📋 Example Session

```
================================================================================
                    SMART Q&A RAG PIPELINE
                         Powered by CrewAI
================================================================================

✓ System Ready!

How to use:
  - Type your question and press Enter
  - The RAG pipeline will search your documents
  - Get an answer with confidence score and sources
  - Type 'quit' or 'exit' to stop

--------------------------------------------------------------------------------

🤔 Your Question: What is machine learning?

================================================================================
⏳ Processing your question...
================================================================================

Agent Workflow:
  [1/3] Document Retriever → Searching ChromaDB...
  [2/3] Answer Writer → Synthesizing answer...
  [3/3] Quality Checker → Verifying and scoring...


[Agent logs will appear here...]


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
  Supported by: sample_ml_basics.txt

FINAL ANSWER WITH HIGHLIGHTED SOURCES:

Machine learning is a subset of artificial intelligence (AI) that focuses on 
developing algorithms and statistical models that enable computer systems to 
improve their performance on tasks through experience...

[SOURCE PARAGRAPH HIGHLIGHTED]
"Machine learning is a subset of artificial intelligence (AI) that focuses on 
developing algorithms and statistical models..."
================================================================================
```

## 🎯 Tips for Best Results

### Document Preparation
- **Format**: PDF or TXT files work best
- **Size**: Keep documents under 10MB each
- **Content**: Clear, well-structured text improves accuracy
- **Language**: English works best (other languages may vary)

### Asking Questions
- ✅ **Be specific**: "What are the types of supervised learning?"
- ✅ **Use keywords**: "machine learning applications"
- ✅ **Reference topics**: "explain overfitting from the document"
- ❌ **Too vague**: "tell me everything"
- ❌ **Outside scope**: Questions not covered in documents

### Troubleshooting

**Issue: "GOOGLE_API_KEY not found"**
```bash
# Check if .env exists
dir .env

# If not, create it
copy .env.example .env

# Edit and add your API key
```

**Issue: "No documents found"**
```bash
# Check docs folder
dir docs

# Add a document if empty
# Then rebuild vector store
python rag_setup.py --force-rebuild
```

**Issue: "Module not found"**
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

## 🔧 Advanced Usage

### Process Multiple Documents
Just drop more PDF/TXT files into the `docs/` folder and run:
```bash
python rag_setup.py
```

### Force Rebuild Vector Store
If you've updated documents:
```bash
python rag_setup.py --force_rebuild=True
```

### Use Different LLM Temperature
Edit `agents.py` and change:
```python
temperature=0.7  # Higher = more creative, Lower = more focused
```

### Change Chunk Size
Edit `rag_setup.py`:
```python
chunk_size=500    # Smaller chunks = more precise retrieval
chunk_overlap=100 # Adjust overlap as needed
```

## 📊 Understanding the Output

### Confidence Score
- **90-100%**: Excellent match, highly reliable
- **70-89%**: Good match, generally reliable
- **50-69%**: Moderate match, verify with sources
- **Below 50%**: Weak match, use caution

### Quality Indicators
- **Factual Accuracy ✓**: Answer matches source material
- **Completeness ✓**: Fully addresses the question
- **Source Support ✓**: All claims backed by retrieved chunks
- **No Hallucination ✓**: No fabricated information

## 🆘 Getting Help

If you encounter issues:
1. Check the README.md for detailed documentation
2. Verify all dependencies are installed
3. Ensure GOOGLE_API_KEY is set correctly
4. Confirm documents are in the docs/ folder
5. Rebuild the vector store

## 🎉 Next Steps

Now that your RAG pipeline is working:

1. **Add your own documents** to the `docs/` folder
2. **Customize agents** in `agents.py` to match your needs
3. **Adjust prompts** in `tasks.py` for different output styles
4. **Experiment with settings** to optimize for your use case

---

**Happy Querying! 🚀**

For more details, see the full README.md file.
