import streamlit as st
from search_engine import ExaSearchEngine
from typing import Dict, Any

def format_result(result: Dict[str, Any]) -> None:
    """Format and display a single search result"""
    title = result.get('title', 'No Title')
    url = result.get('url', '#')
    score = result.get('score', 0.0)
    
    st.markdown(f"### [{title}]({url})")
    st.markdown(f"**Score:** {score:.4f}")
    
    if result.get('author'):
        st.markdown(f"**Author:** {result['author']}")
    
    if result.get('publishedDate'):
        st.markdown(f"**Published:** {result['publishedDate']}")
    
    if result.get('text'):
        with st.expander("Show Content"):
            st.markdown(result['text'])
    
    if result.get('highlights'):
        with st.expander("Show Highlights"):
            for idx, highlight in enumerate(result['highlights']):
                st.markdown(f"{idx + 1}. {highlight}")
    
    st.markdown("---")

def main():
    st.title("EXA Search Pipeline")
    
    # Initialize search engine
    search_engine = ExaSearchEngine()
    
    # Search options
    search_type = st.radio(
        "Select Search Type",
        ["Basic Search", "Advanced Search", "Similar Documents"]
    )
    
    if search_type in ["Basic Search", "Advanced Search"]:
        query = st.text_area("Enter your search query", height=200)
        default_results = 25 if search_type == "Basic Search" else 50
        num_results = st.slider("Number of results", min_value=1, max_value=100, value=default_results)
        
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
                            for result in results:
                                format_result(result)
                        else:
                            st.warning("No results found.")
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
            else:
                st.warning("Please enter a search query")
    
    else:  # Similar Documents
        url = st.text_input("Enter URL to find similar documents")
        num_results = st.slider("Number of results", min_value=1, max_value=100, value=25)
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
                            for result in results:
                                format_result(result)
                        else:
                            st.warning("No similar documents found.")
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
            else:
                st.warning("Please enter a URL")

if __name__ == "__main__":
    main()
