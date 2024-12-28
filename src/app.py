import streamlit as st
from search_engine import ExaSearchEngine
import altair as alt
import pandas as pd
from typing import Dict, Any, List, Tuple

def display_metrics(search_engine: ExaSearchEngine):
    """Display search metrics"""
    metrics = search_engine.get_metrics()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Positive Feedback Rate", f"{metrics['positive_feedback_rate']:.2%}")
    with col2:
        st.metric("Average AI Score", f"{metrics['average_ai_score']:.2f}")
    with col3:
        st.metric("Total Queries", metrics['total_queries'])

def format_result(search_engine: ExaSearchEngine, query: str, 
                 result_tuple: Tuple[Dict[str, Any], float], idx: int) -> None:
    """Format and display a single search result with feedback collection"""
    result, ai_score = result_tuple
    
    # Display result content
    st.markdown(f"### [{result['title']}]({result['url']})")
    st.markdown(f"**Score:** {result['score']:.4f} (AI Relevance: {ai_score:.4f})")
    
    if result.get('author'):
        st.markdown(f"**Author:** {result['author']}")
    
    if result.get('publishedDate'):
        st.markdown(f"**Published:** {result['publishedDate']}")
    
    if result.get('text'):
        with st.expander("Show Content"):
            st.markdown(result['text'])
    
    if result.get('highlights'):
        with st.expander("Show Highlights"):
            for i, highlight in enumerate(result['highlights']):
                st.markdown(f"{i + 1}. {highlight}")
    
    # Collect user feedback
    feedback = st.radio(
        f"Rate Result #{idx + 1}",
        ['Thumbs Up', 'Neutral', 'Thumbs Down'],
        key=f"feedback_{idx}",
        horizontal=True
    )
    
    if st.button(f"Submit Feedback #{idx + 1}", key=f"submit_{idx}"):
        if search_engine.add_feedback(query, result, feedback, ai_score):
            st.success("Feedback recorded!")
        else:
            st.error("Failed to record feedback")
    
    st.markdown("---")

def main():
    st.title("RLAIF Search Pipeline")
    
    # Initialize search engine
    search_engine = ExaSearchEngine()
    
    # Display metrics at the top
    if st.checkbox("Show Search Metrics"):
        display_metrics(search_engine)
    
    # Search options
    search_type = st.radio(
        "Select Search Type",
        ["Basic Search", "Advanced Search", "Similar Documents"]
    )
    
    if search_type in ["Basic Search", "Advanced Search"]:
        query = st.text_input("Enter your search query")
        num_results = st.slider("Number of results", 1, 10, 5)
        
        if search_type == "Advanced Search":
            include_text = st.checkbox("Include full text", value=True)
            include_highlights = st.checkbox("Include highlights", value=True)
            category = st.selectbox(
                "Select category (optional)",
                [None, "company", "research paper", "news", "linkedin profile", 
                 "github", "tweet", "movie", "song", "personal site", "pdf", "financial report"]
            )
        
        if st.button("Search"):
            if query:
                with st.spinner("Searching..."):
                    try:
                        if search_type == "Basic Search":
                            results = search_engine.basic_search(query, num_results)
                        else:
                            results = search_engine.advanced_search(
                                query,
                                num_results,
                                include_text,
                                include_highlights,
                                category
                            )
                        
                        if results:
                            for idx, result_tuple in enumerate(results):
                                format_result(search_engine, query, result_tuple, idx)
                        else:
                            st.warning("No results found.")
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
            else:
                st.warning("Please enter a search query")
    
    else:  # Similar Documents
        url = st.text_input("Enter URL to find similar documents")
        num_results = st.slider("Number of results", 1, 10, 5)
        exclude_source = st.checkbox("Exclude source domain", value=True)
        
        if st.button("Find Similar"):
            if url:
                with st.spinner("Searching for similar documents..."):
                    try:
                        results = search_engine.find_similar_documents(
                            url,
                            num_results,
                            exclude_source
                        )
                        
                        if results:
                            for idx, result_tuple in enumerate(results):
                                format_result(search_engine, url, result_tuple, idx)
                        else:
                            st.warning("No similar documents found.")
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
            else:
                st.warning("Please enter a URL")

if __name__ == "__main__":
    main()
