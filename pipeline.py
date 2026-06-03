# pipeline.py
from similarity import get_top_matches
from granite_analyzer import analyze_writing_style

def analyze_submission(text):
    matches = get_top_matches(text, top_k=3)
    style_analysis = analyze_writing_style(text)

    highest_match = matches[0]['score'] if matches else 0
    ai_prob = style_analysis.get('ai_probability', 0)

    if highest_match > 0.85 or ai_prob > 0.7:
        risk_level = "HIGH"
    elif highest_match > 0.65 or ai_prob > 0.45:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return {
        "risk_level": risk_level,
        "semantic_match_score": highest_match,
        "top_matches": matches,
        "style_analysis": style_analysis
    }