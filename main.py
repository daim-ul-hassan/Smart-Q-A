"""
Main Entry Point - RAG Pipeline with CrewAI
User types questions here and gets answers with source verification
"""

from crew import run_crew
import os
from dotenv import load_dotenv


def load_environment():
    """Load environment variables from .env file"""
    load_dotenv()
    
    if not os.getenv("GOOGLE_API_KEY"):
        print("\n" + "="*60)
        print("WARNING: GOOGLE_API_KEY not found!")
        print("="*60)
        print("""
To get your Google Gemini API key:
1. Go to https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Create a new API key
4. Copy the API key
5. Create a .env file in this directory with:
   GOOGLE_API_KEY=your_api_key_here
""")
        return False
    return True


def display_result(result):
    """Format and display the final result beautifully"""
    print("\n\n" + "="*80)
    print(" " * 25 + "FINAL ANSWER")
    print("="*80)
    
    # Parse and display the result
    result_str = str(result)
    
    # Try to highlight different sections if they exist
    sections = ["CONFIDENCE SCORE", "QUALITY ASSESSMENT", "SOURCE VERIFICATION", 
                "FINAL ANSWER WITH HIGHLIGHTED SOURCES"]
    
    found_sections = []
    for section in sections:
        if section in result_str:
            found_sections.append(section)
    
    if found_sections:
        # Display each section
        for i, section in enumerate(found_sections):
            start_idx = result_str.find(section)
            if i < len(found_sections) - 1:
                end_idx = result_str.find(found_sections[i+1])
            else:
                end_idx = len(result_str)
            
            section_content = result_str[start_idx:end_idx].strip()
            print(f"\n{section_content}")
            print("-"*80)
    else:
        # If no clear sections, just display the full result
        print(result_str)
    
    print("="*80)


def main():
    """Main function - interactive Q&A loop"""
    print("\n" + "="*80)
    print(" " * 20 + "SMART Q&A RAG PIPELINE")
    print(" " * 25 + "Powered by CrewAI")
    print("="*80)
    
    # Load environment variables
    if not load_environment():
        print("\nPlease set up your GOOGLE_API_KEY and try again.")
        return
    
    # Check if vector store exists
    if not os.path.exists("chroma_db"):
        print("\n" + "="*60)
        print("WARNING: Vector store not found!")
        print("="*60)
        print("""
Before asking questions, you need to build the vector store:

1. Add your PDF or TXT files to the 'docs/' folder
2. Run: python rag_setup.py

This will:
- Load all documents from docs/
- Split them into chunks
- Create embeddings
- Store in ChromaDB vector store
""")
        
        response = input("\nDo you want to run rag_setup.py now? (y/n): ").strip().lower()
        if response == 'y':
            import subprocess
            subprocess.run(["python", "rag_setup.py"])
        else:
            print("\nExiting. Please run rag_setup.py when ready.")
            return
    
    print("\n✓ System Ready!")
    print("\nHow to use:")
    print("  - Type your question and press Enter")
    print("  - The RAG pipeline will search your documents")
    print("  - Get an answer with confidence score and sources")
    print("  - Type 'quit' or 'exit' to stop\n")
    
    # Interactive loop
    while True:
        print("-"*80)
        question = input("\n🤔 Your Question: ").strip()
        
        if not question:
            print("⚠️  Please enter a valid question.")
            continue
        
        if question.lower() in ['quit', 'exit', 'q']:
            print("\n\nThank you for using Smart Q&A RAG Pipeline!")
            print("Goodbye! 👋\n")
            break
        
        print("\n" + "="*80)
        print("⏳ Processing your question...")
        print("="*80)
        print("\nAgent Workflow:")
        print("  [1/3] Document Retriever → Searching ChromaDB...")
        print("  [2/3] Answer Writer → Synthesizing answer...")
        print("  [3/3] Quality Checker → Verifying and scoring...\n")
        
        try:
            # Run the crew
            result = run_crew(question)
            
            # Display the result
            display_result(result)
            
        except Exception as e:
            print("\n" + "="*60)
            print("ERROR: An error occurred while processing your question")
            print("="*60)
            print(f"\nError details: {str(e)}")
            print("\nTroubleshooting tips:")
            print("  1. Make sure you have documents in the docs/ folder")
            print("  2. Verify the vector store is built (run rag_setup.py)")
            print("  3. Check your GOOGLE_API_KEY is valid")
            print("  4. Ensure all dependencies are installed")
    
    print("\n" + "="*80)


if __name__ == "__main__":
    main()
