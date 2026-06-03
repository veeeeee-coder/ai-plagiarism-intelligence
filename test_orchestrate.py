from orchestrate_integration import PlagiarismWorkflow

print("🧪 Testing Orchestrate Workflow...")

workflow = PlagiarismWorkflow()

# Test 1: LOW risk submission
print("\n1. LOW risk submission:")
submission = {
    'text': 'This is a completely original essay about my personal experience with climate change. I visited the beach last summer and saw erosion firsthand.',
    'student_id': 'STU001',
    'course': 'ENV101'
}

result = workflow.run_full_workflow(submission)
print(f"   Route: {result['route']}")
print(f"   Priority: {result['priority']}")

# Test 2: HIGH risk submission (with feedback)
print("\n2. HIGH risk submission:")
submission2 = {
    'text': 'Climate change is one of the most pressing issues facing our planet today. The Earth\'s average temperature has risen by about 1.1 degrees Celsius since the late 19th century.',
    'student_id': 'STU002',
    'course': 'ENV101'
}

result2 = workflow.run_full_workflow(submission2, instructor_correction='clean')
print(f"   Route: {result2['route']}")
print(f"   Priority: {result2['priority']}")

print("\n✅ Orchestrate workflow test complete!")