import json
import os
from typing import Dict, List, Any
from datetime import datetime

class FeedbackStore:
    def __init__(self, feedback_file: str = "feedback_log.json"):
        self.feedback_file = feedback_file
        self._initialize_store()
    
    def _initialize_store(self):
        """Initialize the feedback store if it doesn't exist"""
        if not os.path.exists(self.feedback_file):
            with open(self.feedback_file, 'w') as f:
                json.dump([], f)
    
    def add_feedback(self, query: str, result: Dict[str, Any], feedback: str, ai_score: float = None):
        """Add feedback for a search result"""
        feedback_entry = {
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'result': result,
            'user_feedback': feedback,
            'ai_score': ai_score
        }
        
        try:
            with open(self.feedback_file, 'r') as f:
                feedback_log = json.load(f)
            
            feedback_log.append(feedback_entry)
            
            with open(self.feedback_file, 'w') as f:
                json.dump(feedback_log, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving feedback: {str(e)}")
            return False
    
    def get_feedback_history(self) -> List[Dict[str, Any]]:
        """Get all feedback history"""
        try:
            with open(self.feedback_file, 'r') as f:
                return json.load(f)
        except Exception:
            return []
    
    def get_metrics(self) -> Dict[str, float]:
        """Calculate feedback metrics"""
        feedback_log = self.get_feedback_history()
        
        total_entries = len(feedback_log)
        if total_entries == 0:
            return {
                'positive_feedback_rate': 0.0,
                'average_ai_score': 0.0,
                'total_queries': 0
            }
        
        positive_feedback = sum(1 for entry in feedback_log 
                              if entry['user_feedback'] == 'Thumbs Up')
        
        ai_scores = [entry['ai_score'] for entry in feedback_log 
                    if entry['ai_score'] is not None]
        
        unique_queries = len(set(entry['query'] for entry in feedback_log))
        
        return {
            'positive_feedback_rate': positive_feedback / total_entries,
            'average_ai_score': sum(ai_scores) / len(ai_scores) if ai_scores else 0.0,
            'total_queries': unique_queries
        }
