from adaptive_learning import AdaptivePlagiarismDetector

print("🧪 Testing Adaptive Learning...")

detector = AdaptivePlagiarismDetector()

# Test 1: Default thresholds
print(f"\n1. Default thresholds:")
print(f"   High risk similarity: {detector.thresholds['high_risk_similarity']}")
print(f"   High risk AI: {detector.thresholds['high_risk_ai']}")

# Test 2: Risk classification
print(f"\n2. Risk classification tests:")
print(f"   sim=0.9, ai=0.8 → {detector.get_risk_level(0.9, 0.8)}")  # HIGH
print(f"   sim=0.7, ai=0.5 → {detector.get_risk_level(0.7, 0.5)}")  # MEDIUM
print(f"   sim=0.5, ai=0.2 → {detector.get_risk_level(0.5, 0.2)}")  # LOW

# Test 3: Generate report
print(f"\n3. Insight report:")
report = detector.generate_insight_report()
print(report)

# Test 4: Simulate learning (if you have feedback data)
print(f"\n4. Learning from feedback:")
result = detector.learn_from_feedback()
if result:
    print(f"   FP rate: {result['false_positive_rate']:.2%}")
    print(f"   FN rate: {result['false_negative_rate']:.2%}")
    print(f"   Total feedback: {result['total_feedback']}")
else:
    print("   No feedback data yet (need 5+ corrections)")

print("\n✅ Adaptive learning test complete!")