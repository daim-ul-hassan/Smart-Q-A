"""
Crew - Assembles and runs the full RAG pipeline crew
Uses sequential process with context injection between tasks
"""

from crewai import Crew, Process
from agents import create_all_agents
from tasks import create_all_tasks


def create_rag_crew():
    """
    Create and configure the complete RAG pipeline crew
    
    Returns:
        Crew: Configured CrewAI instance with all agents and tasks
    """
    print("Creating RAG Pipeline Crew...")
    
    # Create all agents
    agents = create_all_agents()
    document_retriever = agents["document_retriever"]
    answer_writer = agents["answer_writer"]
    quality_checker = agents["quality_checker"]
    
    print(f"✓ Created 3 agents:")
    print(f"  - {document_retriever.role}")
    print(f"  - {answer_writer.role}")
    print(f"  - {quality_checker.role}")
    
    # Create all tasks
    tasks_dict = create_all_tasks(
        document_retriever=document_retriever,
        answer_writer=answer_writer,
        quality_checker=quality_checker
    )
    
    document_retrieval_task = tasks_dict["document_retrieval"]
    answer_writing_task = tasks_dict["answer_writing"]
    quality_checking_task = tasks_dict["quality_checking"]
    
    print(f"\n✓ Created 3 tasks:")
    print(f"  - Document Retrieval Task")
    print(f"  - Answer Writing Task")
    print(f"  - Quality Checking Task")
    
    # Assemble the crew
    crew = Crew(
        agents=[
            document_retriever,
            answer_writer,
            quality_checker
        ],
        tasks=[
            document_retrieval_task,
            answer_writing_task,
            quality_checking_task
        ],
        process=Process.sequential,  # Sequential execution as specified
        verbose=True,
        memory=True  # Enable crew-level memory for context retention
    )
    
    print("\n✓ RAG Pipeline Crew assembled successfully!")
    print("\nExecution Order:")
    print("  1. Document Retriever → Searches ChromaDB")
    print("  2. Answer Writer → Synthesizes answer from chunks")
    print("  3. Quality Checker → Verifies and provides confidence score")
    
    return crew


def run_crew(question):
    """
    Run the crew with a specific question
    
    Args:
        question (str): User's question
        
    Returns:
        str: Final output from the crew
    """
    crew = create_rag_crew()
    
    print("\n" + "="*60)
    print(f"RUNNING CREW WITH QUESTION:")
    print(f"'{question}'")
    print("="*60)
    
    # Execute the crew
    result = crew.kickoff(inputs={"question": question})
    
    print("\n" + "="*60)
    print("CREW EXECUTION COMPLETED!")
    print("="*60)
    
    return result


if __name__ == "__main__":
    # Test the crew
    test_question = "What is machine learning?"
    print("\nTesting Crew with sample question...")
    print(f"Question: {test_question}\n")
    
    try:
        result = run_crew(test_question)
        print("\n\nFINAL RESULT:")
        print(result)
    except Exception as e:
        print(f"\n✗ Error running crew: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure you have run rag_setup.py to build the vector store")
        print("2. Check that GOOGLE_API_KEY is set in your .env file")
        print("3. Verify all dependencies are installed")
