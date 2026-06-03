# Adaptive learning - the system actually improves from feedback
import json
import os
import numpy as np
from datetime import datetime
from sentence_transformers import SentenceTransformer

FEEDBACK_FILE = 'data/instructor_feedback.json'
THRESHOLD_FILE = 'data/adaptive_thresholds.json'

class AdaptivePlagiarismDetector:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.load_thresholds()
    
    def load_thresholds(self):
        """Load learned thresholds"""
        if os.path.exists(THRESHOLD_FILE):
            with open(THRESHOLD_FILE) as f:
                self.thresholds = json.load(f)
        else:
            # Default thresholds
            self.thresholds = {
                'high_risk_similarity': 0.85,
                'high_risk_ai': 0.7,
                'medium_risk_similarity': 0.65,
                'medium_risk_ai': 0.45,
                'instructor_correction_rate': 0.0,
                'false_positive_rate': 0.0
            }
    
    def save_thresholds(self):
        """Save learned thresholds"""
        with open(THRESHOLD_FILE, 'w') as f:
            json.dump(self.thresholds, f, indent=2)
    
    def learn_from_feedback(self):
        """Adjust thresholds based on instructor corrections"""
        
        if not os.path.exists(FEEDBACK_FILE):
            return
        
        with open(FEEDBACK_FILE) as f:
            feedback = json.load(f)
        
        if len(feedback) < 5:  # Need minimum data
            return
        
        # Analyze patterns
        false_positives = [f for f in feedback 
                          if f['original_verdict'] == 'HIGH' 
                          and f['instructor_correction'] == 'clean']
        
        false_negatives = [f for f in feedback 
                          if f['original_verdict'] == 'LOW' 
                          and f['instructor_correction'] == 'flagged']
        
        fp_rate = len(false_positives) / len(feedback)
        fn_rate = len(false_negatives) / len(feedback)
        
        # Adapt thresholds
        if fp_rate > 0.2:  # Too many false alarms
            self.thresholds['high_risk_similarity'] += 0.05
            self.thresholds['high_risk_ai'] += 0.05
            print("🔄 Adjusted: Raised thresholds to reduce false positives")
        
        if fn_rate > 0.2:  # Missing too many
            self.thresholds['high_risk_similarity'] -= 0.05
            self.thresholds['high_risk_ai'] -= 0.05
            print("🔄 Adjusted: Lowered thresholds to catch more cases")
        
        self.thresholds['false_positive_rate'] = fp_rate
        self.thresholds['instructor_correction_rate'] = len(feedback) / 100
        
        self.save_thresholds()
        
        return {
            'false_positive_rate': fp_rate,
            'false_negative_rate': fn_rate,
            'thresholds_adjusted': True,
            'total_feedback': len(feedback)
        }
    
    def get_risk_level(self, similarity_score, ai_probability):
        """Use adaptive thresholds"""
        hr_sim = self.thresholds['high_risk_similarity']
        hr_ai = self.thresholds['high_risk_ai']
        mr_sim = self.thresholds['medium_risk_similarity']
        mr_ai = self.thresholds['medium_risk_ai']
        
        if similarity_score > hr_sim or ai_probability > hr_ai:
            return "HIGH"
        elif similarity_score > mr_sim or ai_probability > mr_ai:
            return "MEDIUM"
        else:
            return "LOW"
    
    def generate_insight_report(self):
        """Generate analytics for instructors"""
        
        if not os.path.exists(FEEDBACK_FILE):
            return "No feedback data yet."
        
        with open(FEEDBACK_FILE) as f:
            feedback = json.load(f)
        
        # Time-based analysis
        recent = [f for f in feedback 
                 if (datetime.now() - datetime.fromisoformat(f['timestamp'])).days < 30]
        
        report = f"""
## 📊 Adaptive Learning Report

**Total Feedback Processed:** {len(feedback)}
**Recent (30 days):** {len(recent)}

**System Accuracy Trends:**
- False Positive Rate: {self.thresholds['false_positive_rate']:.1%}
- Current High-Risk Threshold: {self.thresholds['high_risk_similarity']:.2f}

**Key Insights:**
- System has {'improved' if self.thresholds['false_positive_rate'] < 0.15 else 'needs tuning'} based on instructor input
- {'Thresholds auto-adjusted' if len(feedback) > 10 else 'Collecting more data for optimization'}

**Recommendation:** 
{'System is production-ready' if self.thresholds['false_positive_rate'] < 0.1 else 'Continue feedback loop for 2 more weeks'}
"""
        return report