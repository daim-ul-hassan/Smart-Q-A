"""
Tasks - Definition of all three tasks for the RAG pipeline
1. Document Retrieval Task - Retrieves relevant chunks from ChromaDB
2. Answer Writing Task - Writes comprehensive answer based on retrieved chunks
3. Quality Checking Task - Verifies answer and provides confidence score
"""

from crewai import Task


def create_document_retrieval_task(agent):
    """
    Create Document Retrieval Task
    This task searches ChromaDB and retrieves relevant chunks
    """
    return Task(
        description="""
        Use the RAG Search Tool to find relevant information in the document database.
        
        User Question: {question}
        
        Steps:
        1. Search ChromaDB using the RAG Search Tool with the user's question
        2. Retrieve the top 3 most relevant chunks
        3. Return complete chunks with source metadata
        
        Make sure to capture:
        - The content of each chunk
        - Source file name
        - Page number (if available)
        - Relevance scores
        """,
        expected_output="""
        A structured response containing:
        - 3 relevant chunks from the document database
        - Each chunk with its content, source, and relevance score
        - Complete metadata for citation purposes
        """,
        agent=agent,
        allow_delegation=False,
        verbose=True,
        human_input=False
    )


def create_answer_writing_task(agent):
    """
    Create Answer Writing Task
    This task synthesizes a comprehensive answer from retrieved chunks
    """
    return Task(
        description="""
        Write a comprehensive answer based ONLY on the retrieved document chunks.
        
        User Question: {question}
        Retrieved Chunks: {context}
        
        Guidelines:
        1. Read through all retrieved chunks carefully
        2. Synthesize information into a coherent answer
        3. Base your answer ONLY on the provided chunks - do not add external knowledge
        4. Structure the answer clearly with proper paragraphs
        5. Include specific details and facts from the chunks
        6. If chunks don't contain enough information, acknowledge this limitation
        
        Important: Your answer must be grounded in the retrieved context!
        """,
        expected_output="""
        A well-structured answer that includes:
        - Direct answer to the user's question
        - Supporting details from the chunks
        - Clear indication of which sources were used
        - Proper citations mentioning source files
        """,
        agent=agent,
        allow_delegation=False,
        verbose=True,
        human_input=False,
        context=[create_document_retrieval_task]  # Context injection from previous task
    )


def create_quality_checking_task(agent):
    """
    Create Quality Checking Task
    This task verifies answer quality and provides confidence scores
    """
    return Task(
        description="""
        Perform quality assurance on the generated answer.
        
        User Question: {question}
        Original Answer: {answer}
        Retrieved Chunks: {context}
        
        Evaluation Criteria:
        1. FACTUAL ACCURACY: Does the answer accurately reflect information from the chunks?
        2. COMPLETENESS: Does the answer fully address the question?
        3. SOURCE SUPPORT: Is every claim in the answer backed by retrieved chunks?
        4. NO HALLUCINATION: Are there any unsupported claims or fabrications?
        
        Tasks:
        1. Compare each statement in the answer against the original chunks
        2. Identify which parts are directly supported by sources
        3. Flag any unsupported claims or extrapolations
        4. Calculate an overall confidence score (0-100%)
        5. Highlight the exact source paragraphs that support the answer
        """,
        expected_output="""
        A detailed quality report containing:
        
        1. CONFIDENCE SCORE: Overall confidence percentage (0-100%)
        
        2. QUALITY ASSESSMENT:
           - Factual Accuracy: ✓/✗
           - Completeness: ✓/✗
           - Source Support: ✓/✗
           - No Hallucination: ✓/✗
        
        3. SOURCE VERIFICATION:
           - List which chunks support which parts of the answer
           - Highlight exact quotes from sources
        
        4. FINAL ANSWER WITH HIGHLIGHTED SOURCES:
           Present the final answer with clear indication of source paragraphs
        """,
        agent=agent,
        allow_delegation=False,
        verbose=True,
        human_input=False,
        context=[create_document_retrieval_task, create_answer_writing_task]  # Full context
    )


def create_all_tasks(document_retriever, answer_writer, quality_checker):
    """Factory function to create all three tasks"""
    return {
        "document_retrieval": create_document_retrieval_task(document_retriever),
        "answer_writing": create_answer_writing_task(answer_writer),
        "quality_checking": create_quality_checking_task(quality_checker)
    }


if __name__ == "__main__":
    print("Task definitions loaded successfully!")
    print("\nTo use these tasks, import them and pass the appropriate agents:")
    print("  from agents import create_all_agents")
    print("  from tasks import create_all_tasks")
    print("  agents = create_all_agents()")
    print("  tasks = create_all_tasks(agents['document_retriever'], ...)")
