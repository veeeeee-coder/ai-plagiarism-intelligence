# feedback_store.py
import json
import os
from datetime import datetime

FEEDBACK_FILE = 'data/instructor_feedback.json'

def save_feedback(submission_hash, original_verdict, instructor_correction, notes=""):
    feedback = []
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE) as f:
            feedback = json.load(f)

    feedback.append({
        "hash": submission_hash,
        "original_verdict": original_verdict,
        "instructor_correction": instructor_correction,
        "notes": notes,
        "timestamp": datetime.now().isoformat()
    })

    with open(FEEDBACK_FILE, 'w') as f:
        json.dump(feedback, f, indent=2)

def get_feedback_stats():
    if not os.path.exists(FEEDBACK_FILE):
        return {"total": 0, "false_positives": 0, "false_negatives": 0}
    with open(FEEDBACK_FILE) as f:
        feedback = json.load(f)
    fp = sum(1 for x in feedback if x['original_verdict'] == 'HIGH' and x['instructor_correction'] == 'clean')
    fn = sum(1 for x in feedback if x['original_verdict'] == 'LOW' and x['instructor_correction'] == 'flagged')
    return {"total": len(feedback), "false_positives": fp, "false_negatives": fn}