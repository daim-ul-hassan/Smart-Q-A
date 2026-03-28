"""
Agents - Definition of all three RAG agents
1. Document Retriever - Uses RAG Search Tool to find relevant chunks
2. Answer Writer - Uses Gemini LLM + CrewAI memory to write answers
3. Quality Checker - Uses LLM + source comparison to verify answers
"""

from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from rag_tool import create_rag_tool
import os


def get_llm():
    """Get Gemini LLM instance"""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY not found! Please set it in your .env file or environment variables."
        )
    
    return ChatGoogleGenerativeAI(
        model="gemini-pro",
        google_api_key=api_key,
        temperature=0.7,
        verbose=True
    )


def create_document_retriever():
    """
    Create Document Retriever Agent
    This agent searches ChromaDB for relevant chunks using RAG Search Tool
    """
    rag_tool = create_rag_tool(persist_directory="chroma_db")
    
    return Agent(
        role="Document Retriever",
        goal="Find and retrieve the most relevant document chunks from ChromaDB vector store based on user queries",
        backstory="""You are an expert information retrieval specialist. Your expertise is in finding 
        the most relevant pieces of information from a large document database. You use the RAG Search 
        Tool to query ChromaDB and retrieve chunks that best match the user's question. You always 
        provide complete chunks with their source metadata.""",
        tools=[rag_tool],
        allow_delegation=False,
        verbose=True,
        llm=get_llm()
    )


def create_answer_writer():
    """
    Create Answer Writer Agent
    This agent uses Gemini LLM and CrewAI memory to synthesize comprehensive answers
    """
    return Agent(
        role="Answer Writer",
        goal="Synthesize comprehensive and accurate answers based on retrieved document chunks",
        backstory="""You are an expert technical writer and subject matter expert. You excel at 
        taking retrieved information and crafting clear, well-structured answers. You always base 
        your answers on the provided context from the Document Retriever. You maintain conversation 
        history through CrewAI memory to provide contextually relevant responses. Your answers are 
        detailed, accurate, and cite the sources used.""",
        allow_delegation=False,
        verbose=True,
        llm=get_llm(),
        memory=True  # Enable CrewAI memory for context retention
    )


def create_quality_checker():
    """
    Create Quality Checker Agent
    This agent verifies answer quality and provides confidence scores with source comparison
    """
    return Agent(
        role="Quality Checker",
        goal="Verify answer accuracy, completeness, and provide confidence scores with source attribution",
        backstory="""You are a meticulous quality assurance specialist. You review answers critically 
        to ensure they are accurate, complete, and properly sourced. You compare answers against the 
        original retrieved chunks to verify factual correctness. You provide a confidence score and 
        highlight which parts of the answer are directly supported by sources. You identify any gaps 
        or unsupported claims.""",
        allow_delegation=False,
        verbose=True,
        llm=get_llm(),
        memory=True  # Enable memory to access previous context
    )


def create_all_agents():
    """Factory function to create all three agents"""
    return {
        "document_retriever": create_document_retriever(),
        "answer_writer": create_answer_writer(),
        "quality_checker": create_quality_checker()
    }


if __name__ == "__main__":
    # Test agent creation
    print("Creating agents...")
    try:
        agents = create_all_agents()
        print(f"\n✓ Successfully created {len(agents)} agents:")
        for role, agent in agents.items():
            print(f"  - {agent.role}")
    except Exception as e:
        print(f"\n✗ Error creating agents: {e}")
        print("\nMake sure you have:")
        print("1. Set GOOGLE_API_KEY in your .env file")
        print("2. Installed all dependencies (pip install -r requirements.txt)")
