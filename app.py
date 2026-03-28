"""
Streamlit Web Interface for Smart Q&A RAG Pipeline
A beautiful, interactive UI for the CrewAI RAG system
"""

import streamlit as st
from crew import run_crew
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Smart Q&A RAG Pipeline",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .agent-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #1E88E5;
    }
    .result-box {
        background-color: #e3f2fd;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 2px solid #1E88E5;
    }
    .confidence-high {
        color: #2ecc71;
        font-weight: bold;
        font-size: 1.5rem;
    }
    .confidence-medium {
        color: #f39c12;
        font-weight: bold;
        font-size: 1.5rem;
    }
    .confidence-low {
        color: #e74c3c;
        font-weight: bold;
        font-size: 1.5rem;
    }
    .checkmark {
        color: #27ae60;
        font-size: 1.2rem;
    }
    .cross {
        color: #e74c3c;
        font-size: 1.2rem;
    }
</style>
""", unsafe_allow_html=True)


def check_api_key():
    """Check if Google API key is configured"""
    return os.getenv("GOOGLE_API_KEY") is not None


def check_vector_store():
    """Check if ChromaDB vector store exists"""
    return os.path.exists("chroma_db")


def display_agent_workflow():
    """Display the agent workflow visualization"""
    st.markdown("### 🔄 Agent Workflow")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("**Agent 1: Document Retriever**\n\n🔍 Searches ChromaDB\n\n📚 Retrieves chunks")
    
    with col2:
        st.success("**Agent 2: Answer Writer**\n\n✍️ Synthesizes answer\n\n🧠 Uses Gemini LLM")
    
    with col3:
        st.warning("**Agent 3: Quality Checker**\n\n✅ Verifies sources\n\n📊 Confidence score")
    
    st.markdown("---")


def main():
    # Header
    st.markdown('<h1 class="main-header">🤖 Smart Q&A RAG Pipeline</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Powered by CrewAI • Gemini LLM • ChromaDB</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Check API key
        api_key_status = check_api_key()
        if api_key_status:
            st.success("✅ Google API Key: Configured")
        else:
            st.error("❌ Google API Key: Missing")
            st.info("Get your API key from:\nhttps://makersuite.google.com/app/apikey")
        
        # Check vector store
        vector_store_status = check_vector_store()
        if vector_store_status:
            st.success("✅ Vector Store: Ready")
        else:
            st.warning("⚠️ Vector Store: Not Built")
            st.info("Run `python rag_setup.py` to build")
        
        st.divider()
        
        # System info
        st.markdown("### 📊 System Info")
        st.markdown(f"- **Agents:** 3")
        st.markdown(f"- **Process:** Sequential")
        st.markdown(f"- **LLM:** Gemini Pro")
        st.markdown(f"- **Vector DB:** ChromaDB")
        st.markdown(f"- **Memory:** Enabled")
        
        st.divider()
        
        # Quick actions
        st.markdown("### 🚀 Quick Actions")
        if st.button("📦 Build Vector Store", use_container_width=True):
            st.info("Run `python rag_setup.py` in terminal")
        
        if st.button("📝 View Documentation", use_container_width=True):
            st.link_button("View GitHub", "https://github.com/daim-ul-hassan/Smart-Q-A")
    
    # Main content area
    if not api_key_status:
        st.warning("⚠️ **Please configure your Google API Key to continue.**\n\n"
                   "1. Go to https://makersuite.google.com/app/apikey\n"
                   "2. Create an API key\n"
                   "3. Create a `.env` file in the project folder\n"
                   "4. Add: `GOOGLE_API_KEY=your_api_key_here`")
        st.stop()
    
    # Display agent workflow
    display_agent_workflow()
    
    # Question input section
    st.markdown("### ❓ Ask Your Question")
    
    # Initialize session state
    if "question" not in st.session_state:
        st.session_state.question = ""
    if "answer" not in st.session_state:
        st.session_state.answer = None
    if "processing" not in st.session_state:
        st.session_state.processing = False
    
    # Question input
    question = st.text_area(
        "Type your question below:",
        height=100,
        placeholder="e.g., What is machine learning?",
        key="input_question"
    )
    
    col1, col2 = st.columns([3, 1])
    with col1:
        ask_button = st.button("🚀 Get Answer", type="primary", use_container_width=True)
    with col2:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.question = ""
            st.session_state.answer = None
            st.rerun()
    
    # Process question
    if ask_button and question:
        st.session_state.question = question
        st.session_state.processing = True
        
        # Progress indicator
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Show agent workflow animation
        with st.spinner("🤖 Agents are working..."):
            try:
                # Step 1: Document Retrieval
                status_text.text("📊 [1/3] Document Retriever searching ChromaDB...")
                progress_bar.progress(33)
                time.sleep(1)
                
                # Step 2: Answer Writing
                status_text.text("✍️ [2/3] Answer Writer synthesizing response...")
                progress_bar.progress(66)
                time.sleep(1)
                
                # Step 3: Quality Checking
                status_text.text("✅ [3/3] Quality Checker verifying sources...")
                progress_bar.progress(90)
                time.sleep(1)
                
                # Run the crew
                result = run_crew(question)
                
                # Complete progress
                progress_bar.progress(100)
                status_text.text("✅ Complete!")
                
                # Store and display result
                st.session_state.answer = result
                st.session_state.processing = False
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("💡 **Troubleshooting:**\n"
                        "- Make sure you've run `python rag_setup.py`\n"
                        "- Check that documents exist in the docs/ folder\n"
                        "- Verify your API key is correct")
                st.session_state.processing = False
                progress_bar.empty()
                status_text.empty()
    
    # Display answer
    if st.session_state.answer and not st.session_state.processing:
        st.markdown("---")
        st.markdown("### 📋 Final Answer")
        
        result_str = str(st.session_state.answer)
        
        # Parse and display different sections
        if "CONFIDENCE SCORE:" in result_str:
            # Extract confidence score
            start = result_str.find("CONFIDENCE SCORE:") + len("CONFIDENCE SCORE:")
            end = result_str.find("\n", start)
            score = result_str[start:end].strip()
            
            # Determine color based on score
            try:
                score_num = float(score.replace('%', ''))
                if score_num >= 80:
                    score_class = "confidence-high"
                    icon = "🟢"
                elif score_num >= 60:
                    score_class = "confidence-medium"
                    icon = "🟡"
                else:
                    score_class = "confidence-low"
                    icon = "🔴"
            except:
                score_class = ""
                icon = "⚪"
            
            st.markdown(f'<div style="text-align: center; margin: 2rem 0;">'
                        f'<span style="font-size: 1.2rem;">Confidence Level:</span><br>'
                        f'<span class="{score_class}">{icon} {score}</span>'
                        f'</div>', unsafe_allow_html=True)
        
        # Display quality assessment
        if "QUALITY ASSESSMENT:" in result_str:
            st.markdown("### ✅ Quality Assessment")
            
            # Extract quality section
            start = result_str.find("QUALITY ASSESSMENT:")
            end = result_str.find("SOURCE VERIFICATION:", start)
            if end == -1:
                end = result_str.find("FINAL ANSWER", start)
            if end == -1:
                end = len(result_str)
            
            quality_section = result_str[start:end].strip()
            
            # Parse checks
            col1, col2, col3, col4 = st.columns(4)
            
            checks = {
                "Factual Accuracy": "✓" in quality_section and "Factual Accuracy" in quality_section,
                "Completeness": "✓" in quality_section and "Completeness" in quality_section,
                "Source Support": "✓" in quality_section and "Source Support" in quality_section,
                "No Hallucination": "✓" in quality_section and "No Hallucination" in quality_section
            }
            
            with col1:
                st.metric("Factual Accuracy", "✓" if checks["Factual Accuracy"] else "✗")
            with col2:
                st.metric("Completeness", "✓" if checks["Completeness"] else "✗")
            with col3:
                st.metric("Source Support", "✓" if checks["Source Support"] else "✗")
            with col4:
                st.metric("No Hallucination", "✓" if checks["No Hallucination"] else "✗")
        
        # Display final answer
        if "FINAL ANSWER WITH HIGHLIGHTED SOURCES:" in result_str:
            st.markdown("### 📖 Final Answer")
            parts = result_str.split("FINAL ANSWER WITH HIGHLIGHTED SOURCES:")
            if len(parts) > 1:
                final_answer = parts[1].strip()
                st.markdown(f'<div class="result-box">{final_answer}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="result-box">{result_str}</div>', unsafe_allow_html=True)
        
        # Download button
        st.download_button(
            label="📥 Download Answer",
            data=str(st.session_state.answer),
            file_name=f"answer_{int(time.time())}.txt",
            mime="text/plain"
        )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem 0;">
        <p><strong>Smart Q&A RAG Pipeline</strong> | Built with CrewAI + Streamlit</p>
        <p>
            <a href="https://github.com/daim-ul-hassan/Smart-Q-A" target="_blank">GitHub Repository</a> | 
            <a href="https://github.com/daim-ul-hassan/Smart-Q-A/blob/main/README.md" target="_blank">Documentation</a>
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
