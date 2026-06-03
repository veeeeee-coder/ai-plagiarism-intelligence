# app.py
import gradio as gr
from pipeline import analyze_submission
from feedback_store import save_feedback, get_feedback_stats
import hashlib

def check_submission(text, instructor_notes):
    if len(text.strip()) < 100:
        return "Please enter at least 100 characters.", "", "", ""

    result = analyze_submission(text)
    sub_hash = hashlib.md5(text.encode()).hexdigest()

    risk_emoji = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}.get(result['risk_level'], "⚪")
    style = result['style_analysis']

    summary = f"""
## {risk_emoji} Risk Level: {result['risk_level']}

**Semantic Similarity Score:** {result['semantic_match_score']:.2%}
**AI Probability:** {style.get('ai_probability', 'N/A')}
**Paraphrase Risk:** {style.get('paraphrase_risk', 'N/A')}

### Verdict
{style.get('verdict', 'Analysis complete.')}

### Flags Detected
{chr(10).join(f'- {f}' for f in style.get('flags', []))}
"""
    matches_text = "\n".join([f"• [{m['label'].upper()}] Score: {m['score']} — {m['text'][:150]}..." for m in result['top_matches']])
    stats = get_feedback_stats()
    stats_text = f"Total reviewed: {stats['total']} | False positives: {stats['false_positives']} | False negatives: {stats['false_negatives']}"

    return summary, matches_text, stats_text, sub_hash

def submit_feedback(sub_hash, verdict, correction, notes):
    if sub_hash:
        save_feedback(sub_hash, verdict, correction, notes)
        return "✅ Feedback saved. Model will improve with more examples."
    return "No submission to give feedback on."

with gr.Blocks(title="AI Plagiarism Intelligence") as demo:
    gr.Markdown("# 🎓 AI-Driven Plagiarism Intelligence")
    gr.Markdown("Powered by IBM Granite 8B + IBM Slate + watsonx.ai")

    with gr.Row():
        with gr.Column(scale=2):
            text_input = gr.Textbox(label="Paste student submission", lines=10, placeholder="Paste the assignment text here...")
            notes_input = gr.Textbox(label="Instructor context (optional)", placeholder="e.g. This student has dyslexia...")
            check_btn = gr.Button("Analyze Submission", variant="primary")
        with gr.Column(scale=1):
            risk_output = gr.Markdown(label="Analysis Report")
            matches_output = gr.Textbox(label="Top Matching Documents", lines=6)
            stats_output = gr.Textbox(label="System Accuracy Stats", interactive=False)
            hash_state = gr.State()

    gr.Markdown("### 📝 Instructor Feedback")
    with gr.Row():
        verdict_display = gr.Textbox(label="System verdict", interactive=False)
        correction_input = gr.Radio(["clean", "flagged"], label="Your correction")
        feedback_notes = gr.Textbox(label="Notes")
        feedback_btn = gr.Button("Submit Feedback")
        feedback_status = gr.Textbox(label="Status", interactive=False)

    check_btn.click(check_submission, inputs=[text_input, notes_input], outputs=[risk_output, matches_output, stats_output, hash_state])
    feedback_btn.click(submit_feedback, inputs=[hash_state, verdict_display, correction_input, feedback_notes], outputs=[feedback_status])

demo.launch(share=True)