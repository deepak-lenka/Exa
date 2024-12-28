from exa_py import Exa
import os
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional, Tuple
from feedback_store import FeedbackStore

class ExaSearchEngine:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv('EXA_API_KEY')
        if not api_key:
            raise ValueError("EXA_API_KEY environment variable is not set")
        self.exa = Exa(api_key)
        self.feedback_store = FeedbackStore()

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

    def _evaluate_result_relevance(self, query: str, result: Dict[str, Any]) -> float:
        """
        Use Exa to evaluate the relevance of a result to the query
        Returns a score between 0 and 1
        """
        try:
            # Create a prompt for relevance evaluation
            content = f"{result.get('text', '')} {' '.join(result.get('highlights', []))}"
            if not content:
                content = result.get('title', '')

            # Use Exa's neural search to evaluate relevance
            eval_response = self.exa.search(
                f"Rate the relevance of this content to the query '{query}': {content[:500]}",
                type="neural",
                use_autoprompt=True,
                num_results=1
            )
            
            if eval_response and hasattr(eval_response, 'results'):
                # Use the score from Exa's evaluation
                return float(getattr(eval_response.results[0], 'score', 0.5))
            return 0.5
        except Exception:
            return 0.5

    def _rerank_results(self, query: str, results: List[Dict[str, Any]]) -> List[Tuple[Dict[str, Any], float]]:
        """
        Rerank results based on AI feedback
        Returns list of (result, ai_score) tuples
        """
        scored_results = []
        for result in results:
            ai_score = self._evaluate_result_relevance(query, result)
            # Combine original score with AI evaluation
            final_score = (result['score'] * 0.3) + (ai_score * 0.7)
            result['score'] = final_score
            scored_results.append((result, ai_score))
        
        # Sort by final score
        return sorted(scored_results, key=lambda x: x[0]['score'], reverse=True)

    def basic_search(self, query: str, num_results: int = 5) -> List[Tuple[Dict[str, Any], float]]:
        """
        Perform a basic search using Exa's neural search
        Returns list of (result, ai_score) tuples
        """
        try:
            response = self.exa.search(
                query,
                type="neural",
                use_autoprompt=True,
                num_results=num_results
            )
            if response and hasattr(response, 'results'):
                results = [self._convert_result_to_dict(result) for result in response.results]
                return self._rerank_results(query, results)
            return []
        except Exception as e:
            raise Exception(f"Search failed: {str(e)}")

    def advanced_search(self, 
                       query: str,
                       num_results: int = 5,
                       include_text: bool = True,
                       include_highlights: bool = True,
                       category: Optional[str] = None) -> List[Tuple[Dict[str, Any], float]]:
        """
        Perform an advanced search with content retrieval
        Returns list of (result, ai_score) tuples
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
                results = [self._convert_result_to_dict(result) for result in response.results]
                return self._rerank_results(query, results)
            return []
        except Exception as e:
            raise Exception(f"Advanced search failed: {str(e)}")

    def find_similar_documents(self, 
                             url: str,
                             num_results: int = 5,
                             exclude_source: bool = True) -> List[Tuple[Dict[str, Any], float]]:
        """
        Find similar documents based on a URL
        Returns list of (result, ai_score) tuples
        """
        try:
            response = self.exa.find_similar(
                url,
                num_results=num_results,
                exclude_source_domain=exclude_source
            )
            if response and hasattr(response, 'results'):
                results = [self._convert_result_to_dict(result) for result in response.results]
                # For similar documents, use the URL as the query for relevance evaluation
                return self._rerank_results(url, results)
            return []
        except Exception as e:
            raise Exception(f"Similar document search failed: {str(e)}")

    def add_feedback(self, query: str, result: Dict[str, Any], feedback: str, ai_score: float):
        """Add user feedback for a search result"""
        return self.feedback_store.add_feedback(query, result, feedback, ai_score)

    def get_metrics(self) -> Dict[str, float]:
        """Get feedback metrics"""
        return self.feedback_store.get_metrics()
