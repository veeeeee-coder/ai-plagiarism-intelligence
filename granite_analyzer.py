from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai import Credentials
import json
from config import API_KEY, PROJECT_ID

def analyze_writing_style(text):
    credentials = Credentials(
        url="https://au-syd.ml.cloud.ibm.com",
        api_key=API_KEY
    )

    model = ModelInference(
        model_id="ibm/granite-8b-code-instruct",
        credentials=credentials,
        project_id=PROJECT_ID,
        params={
            GenParams.MAX_NEW_TOKENS: 400,
            GenParams.TEMPERATURE: 0.2,
            GenParams.STOP_SEQUENCES: ["###"]
        }
    )

    prompt = f"""You are an academic integrity analyst. Analyze the following student submission for signs of AI-generated content or paraphrasing. 

Look for:
1. Unusual uniformity in sentence length
2. Lack of personal voice or hedging language
3. Overly formal transitions
4. Generic factual statements without personal insight
5. Perfect grammar with no natural errors

Submission:
\"\"\"{text[:1500]}\"\"\"

Respond in JSON format:
{{
  "ai_probability": <0.0 to 1.0>,
  "paraphrase_risk": <"low"/"medium"/"high">,
  "flags": [list of specific observations],
  "verdict": <one sentence summary>
}}
###"""

    response = model.generate_text(prompt=prompt)
    try:
        return json.loads(response)
    except:
        return {"raw_response": response, "ai_probability": 0.5, "flags": ["Parse error"]}