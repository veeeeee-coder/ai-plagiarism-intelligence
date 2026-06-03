from pipeline import analyze_submission

# Test with a sample text
test_text = "Climate change is one of the most pressing issues facing our planet today. The Earth's average temperature has risen by about 1.1 degrees Celsius since the late 19th century."

print("Testing full pipeline...")
result = analyze_submission(test_text)

print(f"\nRisk Level: {result['risk_level']}")
print(f"Semantic Match: {result['semantic_match_score']:.2%}")
print(f"AI Probability: {result['style_analysis'].get('ai_probability', 'N/A')}")
print(f"Verdict: {result['style_analysis'].get('verdict', 'N/A')}")
print(f"Top Matches: {len(result['top_matches'])}")