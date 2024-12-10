import json
from typing import List, Dict
from pathlib import Path

class HighScoreManager:
    def __init__(self):
        self.scores_file = Path("highscores.json")
        self.high_scores = self._load_scores()
    
    def _load_scores(self) -> List[Dict]:
        try:
            if self.scores_file.exists():
                with open(self.scores_file, 'r') as f:
                    return json.load(f)
            else:
                # Create file with empty list if it doesn't exist
                self._save_scores([])
                return []
        except (json.JSONDecodeError, FileNotFoundError):
            # Handle corrupted file or any other issues
            self._save_scores([])
            return []
    
    def _save_scores(self, scores: List[Dict] = None) -> None:
        if scores is None:
            scores = self.high_scores
        
        # Ensure the directory exists
        self.scores_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Write the scores to file
        with open(self.scores_file, 'w') as f:
            json.dump(scores, f, indent=4)
    
    def add_score(self, name: str, score: int) -> bool:
        """Add a new score and return True if it made the top 10"""
        new_entry = {"name": name, "score": score}
        
        # Check if it's a new highest score before adding
        current_highest = self.high_scores[0]['score'] if self.high_scores else 0
        is_new_highest = score > current_highest

        # Add new score and sort
        self.high_scores.append(new_entry)
        self.high_scores.sort(key=lambda x: x["score"], reverse=True)
        
        # Keep only top 5
        self.high_scores = self.high_scores[:5]
        
        # Save to file
        self._save_scores()
        
        # Return True if score is the new highest score
        return is_new_highest
    
    def get_high_scores(self) -> List[Dict]:
        return self.high_scores