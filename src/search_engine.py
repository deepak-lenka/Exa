from exa_py import Exa
import os
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional

class ExaSearchEngine:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv('EXA_API_KEY')
        if not api_key:
            raise ValueError("EXA_API_KEY environment variable is not set")
        self.exa = Exa(api_key)

    def _convert_result_to_dict(self, result) -> Dict[str, Any]:
        """Convert an Exa result object to a dictionary"""
        return {
            'title': getattr(result, 'title', 'No Title'),
            'url': getattr(result, 'url', '#'),
            'score': getattr(result, 'score', 0.0),
            'author': getattr(result, 'author', None),
            'publishedDate': getattr(result, 'published_date', None),
            'text': getattr(result, 'text', None),
            'highlights': getattr(result, 'highlights', [])
        }

    def basic_search(self, query: str, num_results: int = 25) -> List[Dict[str, Any]]:
        """
        Perform a basic search using Exa's neural search
        """
        try:
            response = self.exa.search(
                query,
                type="neural",
                use_autoprompt=True,
                num_results=num_results
            )
            if response and hasattr(response, 'results'):
                return [self._convert_result_to_dict(result) for result in response.results]
            return []
        except Exception as e:
            raise Exception(f"Search failed: {str(e)}")

    def advanced_search(self, 
                       query: str,
                       num_results: int = 50,
                       include_text: bool = True,
                       include_highlights: bool = True,
                       category: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Perform an advanced search with content retrieval
        """
        try:
            response = self.exa.search_and_contents(
                query,
                text=include_text,
                highlights=include_highlights,
                num_results=num_results,
                type="neural",
                use_autoprompt=True,
                category=category
            )
            if response and hasattr(response, 'results'):
                return [self._convert_result_to_dict(result) for result in response.results]
            return []
        except Exception as e:
            raise Exception(f"Advanced search failed: {str(e)}")

    def find_similar_documents(self, 
                             url: str,
                             num_results: int = 5,
                             exclude_source: bool = True) -> List[Dict[str, Any]]:
        """
        Find similar documents based on a URL
        """
        try:
            response = self.exa.find_similar(
                url,
                num_results=num_results,
                exclude_source_domain=exclude_source
            )
            if response and hasattr(response, 'results'):
                return [self._convert_result_to_dict(result) for result in response.results]
            return []
        except Exception as e:
            raise Exception(f"Similar document search failed: {str(e)}")