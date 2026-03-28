# Customization Examples

This guide shows you how to customize different aspects of the RAG pipeline.

## 🎨 1. Customizing Agents

### Change Agent Personality

Edit `agents.py`:

```python
def create_answer_writer():
    return Agent(
        role="Answer Writer",
        goal="Synthesize comprehensive and accurate answers based on retrieved document chunks",
        backstory="""You are a friendly and approachable teacher who loves making complex topics 
        easy to understand. You explain things in simple terms with helpful analogies. You always 
        make sure to cite your sources clearly.""",  # Changed from formal expert to friendly teacher
        allow_delegation=False,
        verbose=True,
        llm=get_llm(),
        memory=True
    )
```

### Adjust LLM Temperature (Creativity vs Focus)

In `agents.py`, modify `get_llm()`:

```python
def get_llm():
    """Get Gemini LLM instance"""
    api_key = os.getenv("GOOGLE_API_KEY")
    
    return ChatGoogleGenerativeAI(
        model="gemini-pro",
        google_api_key=api_key,
        temperature=0.3,  # Lower = more focused/deterministic
        # temperature=0.7,  # Balanced (default)
        # temperature=1.0,  # Higher = more creative/random
        verbose=True
    )
```

**Temperature Guide:**
- `0.1-0.3`: Very focused, good for factual Q&A
- `0.5-0.7`: Balanced, good general purpose
- `0.8-1.0`: More creative, good for brainstorming

## 📝 2. Customizing Tasks

### Modify Task Prompts

Edit `tasks.py` to change how agents behave:

```python
def create_answer_writing_task(agent):
    return Task(
        description="""
        Write a comprehensive answer based ONLY on the retrieved document chunks.
        
        User Question: {question}
        Retrieved Chunks: {context}
        
        IMPORTANT GUIDELINES:
        1. Start with a direct one-sentence answer
        2. Provide 2-3 supporting details
        3. Use bullet points for clarity
        4. End with a summary sentence
        5. Cite specific page numbers when available
        
        FORMAT YOUR ANSWER AS:
        - Direct Answer: [Your response]
        - Key Details:
          * Detail 1
          * Detail 2
        - Summary: [Brief wrap-up]
        """,
        expected_output="Structured answer with clear sections",
        agent=agent,
        allow_delegation=False,
        verbose=True,
        human_input=False,
        context=[create_document_retrieval_task]
    )
```

### Change Number of Retrieved Chunks

Edit `rag_tool.py`:

```python
def _run(self, query: str) -> str:
    if not self.vectordb:
        return "Error: Vector store not available."
    
    try:
        # Change k=3 to retrieve more or fewer chunks
        results = self.vectordb.similarity_search_with_score(query, k=5)  # Changed from 3 to 5
        # ... rest of code
```

## 🔧 3. Customizing Document Processing

### Adjust Chunk Size

Edit `rag_setup.py`:

```python
def __init__(self, docs_folder="docs", persist_directory="chroma_db"):
    self.docs_folder = Path(docs_folder)
    self.persist_directory = persist_directory
    self.chunks_dir = "chunk_cache"
    
    # Customize chunk parameters
    self.text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,      # Smaller chunks (was 1000)
        chunk_overlap=100,   # Less overlap (was 200)
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
```

**Chunk Size Guide:**
- Small (300-500): More precise retrieval, better for specific facts
- Medium (800-1200): Balanced (default)
- Large (1500-2000): More context per chunk, better for complex topics

### Change Embedding Model

Edit both `rag_setup.py` and `rag_tool.py`:

```python
# In rag_setup.py __init__ method
self.embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"  # Better quality, slower
    # model_name="sentence-transformers/all-MiniLM-L6-v2"  # Fast, good quality (default)
    # model_name="BAAI/bge-small-en-v1.5"  # Good alternative
)
```

**Embedding Model Options:**
- `all-MiniLM-L6-v2`: Fast, good quality (recommended default)
- `all-mpnet-base-v2`: Slower but better quality
- `bge-small-en-v1.5`: Good balance, alternative option

## 🎯 4. Changing the Workflow

### Add a Fourth Agent (Example: Summarizer)

Add to `agents.py`:

```python
def create_summarizer():
    return Agent(
        role="Summary Specialist",
        goal="Create concise summaries of verified answers",
        backstory="""You excel at distilling complex information into brief, 
        clear summaries. You focus on the essential points.""",
        allow_delegation=False,
        verbose=True,
        llm=get_llm(),
        memory=True
    )
```

Add corresponding task in `tasks.py`:

```python
def create_summarization_task(agent):
    return Task(
        description="""
        Create a brief summary of the verified answer.
        
        Original Answer: {answer}
        Quality Report: {quality_report}
        
        Create a 2-3 sentence executive summary.
        """,
        expected_output="Concise 2-3 sentence summary",
        agent=agent,
        allow_delegation=False,
        verbose=True,
        context=[create_quality_checking_task]
    )
```

Update `crew.py`:

```python
def create_rag_crew():
    agents = create_all_agents()
    agents["summarizer"] = create_summarizer()  # Add new agent
    
    # ... create tasks ...
    
    crew = Crew(
        agents=[
            agents["document_retriever"],
            agents["answer_writer"],
            agents["quality_checker"],
            agents["summarizer"]  # Add to crew
        ],
        tasks=[
            document_retrieval_task,
            answer_writing_task,
            quality_checking_task,
            summarization_task  # Add task
        ],
        process=Process.sequential,
        verbose=True,
        memory=True
    )
```

## 🎨 5. Output Formatting

### Customize Result Display

Edit `main.py`:

```python
def display_result(result):
    """Format and display the final result beautifully"""
    print("\n\n" + "="*80)
    print(" " * 30 + "📊 RESULTS")
    print("="*80)
    
    result_str = str(result)
    
    # Extract confidence score
    if "CONFIDENCE SCORE:" in result_str:
        start = result_str.find("CONFIDENCE SCORE:") + len("CONFIDENCE SCORE:")
        end = result_str.find("\n", start)
        score = result_str[start:end].strip()
        print(f"\n🎯 Confidence Level: {score}")
        print("-"*80)
    
    # Extract and display final answer
    if "FINAL ANSWER WITH HIGHLIGHTED SOURCES:" in result_str:
        parts = result_str.split("FINAL ANSWER WITH HIGHLIGHTED SOURCES:")
        if len(parts) > 1:
            final_answer = parts[1].strip()
            print("\n💡 Final Answer:")
            print("-"*80)
            print(final_answer)
    
    print("="*80)
```

## 📚 6. Adding Multiple Documents

Just drop files into `docs/` folder:

```bash
docs/
├── machine_learning_basics.txt
├── deep_learning_intro.pdf
├── neural_networks.pdf
└── data_science_guide.txt
```

Then rebuild:

```bash
python rag_setup.py
```

The system automatically processes all PDF and TXT files!

## 🔍 7. Custom Search Parameters

Edit `rag_tool.py` to add advanced search:

```python
def _run(self, query: str) -> str:
    if not self.vectordb:
        return "Error: Vector store not available."
    
    try:
        # Try different search strategies
        results = self.vectordb.similarity_search_with_score(
            query, 
            k=3,
            filter=None  # Add metadata filters here if needed
        )
        
        # Or use maximum marginal relevance for diversity
        # results = self.vectordb.max_marginal_relevance_search(
        #     query, k=3, fetch_k=20, lambda_mult=0.5
        # )
        
        # ... rest of code
```

## ⚙️ 8. Environment-Specific Configurations

Create different config files:

**config_dev.py**:
```python
CHUNK_SIZE = 500
TEMPERATURE = 0.9
VERBOSE = True
```

**config_prod.py**:
```python
CHUNK_SIZE = 1000
TEMPERATURE = 0.5
VERBOSE = False
```

Load in your code:
```python
import os
env = os.getenv("ENVIRONMENT", "production")

if env == "development":
    from config_dev import *
else:
    from config_prod import *
```

## 🎭 9. Domain-Specific Customization

### For Legal Documents:

```python
def create_legal_reviewer():
    return Agent(
        role="Legal Document Analyst",
        goal="Analyze legal documents with precision",
        backstory="""You are a meticulous legal analyst with expertise in 
        contract interpretation and case law analysis.""",
        tools=[rag_tool],
        llm=get_llm()
    )
```

### For Medical Literature:

```python
def create_medical_researcher():
    return Agent(
        role="Medical Research Specialist",
        goal="Extract accurate medical information",
        backstory="""You are a medical researcher with expertise in evidence-based 
        medicine and clinical literature review.""",
        tools=[rag_tool],
        llm=get_llm()
    )
```

### For Technical Documentation:

```python
def create_tech_writer():
    return Agent(
        role="Technical Documentation Expert",
        goal="Explain technical concepts clearly",
        backstory="""You are a senior technical writer specializing in software 
        documentation and API references.""",
        tools=[rag_tool],
        llm=get_llm()
    )
```

## 📊 10. Performance Tuning

### Batch Processing Multiple Questions

Create `batch_query.py`:

```python
from crew import run_crew

questions = [
    "What is machine learning?",
    "How does supervised learning work?",
    "Explain neural networks"
]

for i, question in enumerate(questions, 1):
    print(f"\n{'='*80}")
    print(f"Question {i}/{len(questions)}")
    print(f"{'='*80}")
    result = run_crew(question)
    print(result)
```

Run it:
```bash
python batch_query.py
```

---

## 🧪 Testing Your Changes

After making customizations:

1. **Test with sample questions**:
   ```bash
   python main.py
   ```

2. **Check vector store**:
   ```bash
   python rag_setup.py
   ```

3. **Verify agent creation**:
   ```bash
   python agents.py
   ```

## 💡 Best Practices

✅ **DO**:
- Test changes incrementally
- Keep backups of working configurations
- Document your customizations
- Version control your changes

❌ **DON'T**:
- Change multiple settings at once
- Skip testing after changes
- Forget to commit your .env file to .gitignore
- Ignore error messages

---

**Happy Customizing! 🚀**
