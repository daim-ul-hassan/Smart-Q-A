# 🚀 GET YOUR API KEY & RUN THE SYSTEM

## Step 1: Get Google Gemini API Key (2 minutes)

1. **Go to:** https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the API key

## Step 2: Create .env File

Create a file named `.env` in this folder and add:

```
GOOGLE_API_KEY=paste_your_api_key_here
```

## Step 3: Install Dependencies (Already Done! ✅)

All dependencies are installed. You're ready to go!

## Step 4: Build Vector Store

Open PowerShell/CMD in this folder and run:

```bash
python rag_setup.py
```

This will process all documents in the `docs/` folder.

## Step 5: Start Asking Questions!

```bash
python main.py
```

Then type your question!

---

## Quick Test Commands

```bash
# Check if everything is installed
python --version
pip list | findstr crewai
pip list | findstr chromadb
pip list | findstr langchain

# Run the system
python main.py
```

---

## Sample Questions to Try

Once running, try asking:
- "What is machine learning?"
- "What are the types of machine learning?"
- "Explain supervised learning"

---

**That's it! You're ready to use the Smart Q&A RAG Pipeline! 🎉**
