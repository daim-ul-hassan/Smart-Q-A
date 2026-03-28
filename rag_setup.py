"""
RAG Setup - Document Loading and Vector Store Creation
This script loads PDF and TXT files from docs/ folder, splits them into chunks,
creates embeddings, and stores them in ChromaDB vector store.
"""

import os
from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.schema import Document
import pickle


class RAGSetup:
    def __init__(self, docs_folder="docs", persist_directory="chroma_db"):
        self.docs_folder = Path(docs_folder)
        self.persist_directory = persist_directory
        self.chunks_dir = "chunk_cache"
        
        # Initialize text splitter with optimized chunk parameters
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        
        # Initialize embeddings model
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        # Create cache directory for chunks
        os.makedirs(self.chunks_dir, exist_ok=True)
    
    def load_documents(self):
        """Load all PDF and TXT files from the docs folder"""
        documents = []
        
        if not self.docs_folder.exists():
            print(f"Error: Docs folder '{self.docs_folder}' does not exist!")
            return documents
        
        # Load PDF files
        pdf_files = list(self.docs_folder.glob("*.pdf"))
        for pdf_path in pdf_files:
            print(f"Loading PDF: {pdf_path.name}")
            loader = PyPDFLoader(str(pdf_path))
            documents.extend(loader.load())
        
        # Load TXT files
        txt_files = list(self.docs_folder.glob("*.txt"))
        for txt_path in txt_files:
            print(f"Loading TXT: {txt_path.name}")
            loader = TextLoader(str(txt_path), encoding='utf-8')
            documents.extend(loader.load())
        
        print(f"\nTotal documents loaded: {len(documents)}")
        return documents
    
    def split_documents(self, documents):
        """Split documents into smaller chunks"""
        print("\nSplitting documents into chunks...")
        chunks = self.text_splitter.split_documents(documents)
        print(f"Total chunks created: {len(chunks)}")
        return chunks
    
    def save_chunks(self, chunks, filename="chunks.pkl"):
        """Save chunks to disk for later use"""
        filepath = os.path.join(self.chunks_dir, filename)
        with open(filepath, 'wb') as f:
            pickle.dump(chunks, f)
        print(f"Chunks saved to: {filepath}")
    
    def load_chunks(self, filename="chunks.pkl"):
        """Load chunks from disk"""
        filepath = os.path.join(self.chunks_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                chunks = pickle.load(f)
            print(f"Chunks loaded from: {filepath}")
            return chunks
        else:
            print(f"No chunk cache found at: {filepath}")
            return None
    
    def create_vector_store(self, chunks):
        """Create ChromaDB vector store from chunks"""
        print("\nCreating ChromaDB vector store...")
        print(f"Persist directory: {self.persist_directory}")
        
        # Create and persist the vector store
        vectordb = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        
        print(f"Vector store created successfully!")
        print(f"Total vectors in store: {vectordb._collection.count()}")
        return vectordb
    
    def load_vector_store(self):
        """Load existing ChromaDB vector store"""
        if os.path.exists(self.persist_directory):
            vectordb = Chroma(
                persist_directory=self.persist_directory,
                embedding_model=self.embeddings
            )
            print(f"Vector store loaded from: {self.persist_directory}")
            print(f"Total vectors: {vectordb._collection.count()}")
            return vectordb
        else:
            print(f"No vector store found at: {self.persist_directory}")
            return None
    
    def setup(self, force_rebuild=False):
        """Complete setup pipeline"""
        print("="*60)
        print("RAG SETUP PIPELINE")
        print("="*60)
        
        # Check if we have cached chunks and not forcing rebuild
        if not force_rebuild:
            chunks = self.load_chunks()
            if chunks:
                print("\nUsing cached chunks...")
                vectordb = self.create_vector_store(chunks)
                return vectordb
        
        # Full pipeline
        documents = self.load_documents()
        if not documents:
            print("No documents found! Please add PDF or TXT files to docs/ folder.")
            return None
        
        chunks = self.split_documents(documents)
        self.save_chunks(chunks)
        vectordb = self.create_vector_store(chunks)
        
        return vectordb


def main():
    """Main function to run RAG setup"""
    print("\nStarting RAG Setup...\n")
    
    # Initialize RAG Setup
    rag_setup = RAGSetup(
        docs_folder="docs",
        persist_directory="chroma_db"
    )
    
    # Run setup pipeline
    vectordb = rag_setup.setup(force_rebuild=False)
    
    if vectordb:
        print("\n" + "="*60)
        print("RAG SETUP COMPLETED SUCCESSFULLY!")
        print("="*60)
        print(f"\nYou can now use the vector store in your CrewAI agents.")
        print(f"Vector store location: chroma_db/")
        print(f"Number of chunks: {vectordb._collection.count()}")
    else:
        print("\nRAG Setup failed!")


if __name__ == "__main__":
    main()
