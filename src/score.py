class Score:
    def __init__(self):
        self.value = 0
        self.high_score = 0
        
    def increment(self):
        """Increase score by 1"""
        self.value += 1
        if self.value > self.high_score:
            self.high_score = self.value
            
    def reset(self):
        """Reset current score to 0"""
        self.value = 0
        
    def get_high_score(self):
        """Get high score"""
        return self.high_score
