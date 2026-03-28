"""
RAG Tool - Custom CrewAI Tool for querying ChromaDB
This tool allows agents to search and retrieve relevant chunks from the vector store.
"""

from crewai_tools import BaseTool
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from typing import Type
from pydantic import BaseModel, Field


class RAGSearchInput(BaseModel):
    """Input schema for RAG Search Tool"""
    query: str = Field(description="The search query to find relevant chunks in the vector store")


class RAGSearchTool(BaseTool):
    """Custom CrewAI tool that queries ChromaDB vector store"""
    
    name: str = "RAG Search Tool"
    description: str = """
        Use this tool to search for relevant information in the document database.
        Input should be a question or search query.
        Returns relevant chunks with their source metadata.
    """
    args_schema: Type[BaseModel] = RAGSearchInput
    
    def __init__(self, persist_directory="chroma_db"):
        super().__init__()
        self.persist_directory = persist_directory
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.vectordb = None
        self._load_vector_store()
    
    def _load_vector_store(self):
        """Load the ChromaDB vector store"""
        try:
            self.vectordb = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
            print(f"[RAG Tool] Vector store loaded successfully!")
        except Exception as e:
            print(f"[RAG Tool] Error loading vector store: {e}")
            self.vectordb = None
    
    def _run(self, query: str) -> str:
        """
        Execute the search and return relevant chunks
        
        Args:
            query: The search query
            
        Returns:
            Formatted string containing relevant chunks with sources
        """
        if not self.vectordb:
            return "Error: Vector store not available. Please run rag_setup.py first."
        
        try:
            # Perform similarity search
            results = self.vectordb.similarity_search_with_score(query, k=3)
            
            if not results:
                return "No relevant information found in the document database."
            
            # Format the results
            formatted_results = []
            for i, (doc, score) in enumerate(results, 1):
                chunk_info = f"""
--- Chunk {i} ---
Relevance Score: {score:.4f}
Source: {doc.metadata.get('source', 'Unknown')}
Page: {doc.metadata.get('page', 'N/A')}

Content:
{doc.page_content}
-----------------
"""
                formatted_results.append(chunk_info)
            
            final_output = "\n".join(formatted_results)
            return f"Found {len(results)} relevant chunk(s):\n\n{final_output}"
            
        except Exception as e:
            return f"Error searching vector store: {str(e)}"
    
    async def _arun(self, query: str) -> str:
        """Async version of the tool (not implemented)"""
        raise NotImplementedError("Async operation not supported")


def create_rag_tool(persist_directory="chroma_db"):
    """Factory function to create RAG Search Tool instance"""
    return RAGSearchTool(persist_directory=persist_directory)


if __name__ == "__main__":
    # Test the tool
    print("Testing RAG Search Tool...")
    tool = create_rag_tool()
    
    test_query = "What is machine learning?"
    print(f"\nQuery: {test_query}")
    result = tool._run(test_query)
    print(result)
