# Multi-modal analysis - handles PDFs, images of assignments
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai import Credentials
from config import API_KEY, PROJECT_ID
import base64

def analyze_document_image(image_path):
    """Analyze scanned/image assignments using Granite Vision 3.2"""
    
    credentials = Credentials(
        url="https://au-syd.ml.cloud.ibm.com",
        api_key=API_KEY
    )
    
    # Granite Vision 3.2 - document understanding specialist
    model = ModelInference(
        model_id="ibm/granite-vision-3-2-2b",  # Vision model
        credentials=credentials,
        project_id=PROJECT_ID,
        params={
            GenParams.MAX_NEW_TOKENS: 500,
            GenParams.TEMPERATURE: 0.2
        }
    )
    
    # Read image
    with open(image_path, 'rb') as f:
        img_bytes = f.read()
    
    img_b64 = base64.b64encode(img_bytes).decode('utf-8')
    
    prompt = """Analyze this document image for signs of plagiarism or AI generation.
    Look for:
    1. Inconsistent fonts or formatting (copy-paste from multiple sources)
    2. Perfect formatting without natural errors
    3. Watermarks or metadata suggesting AI tools
    4. Unusual spacing or alignment
    
    Respond in JSON format with findings."""
    
    # For vision models, we pass image data differently
    response = model.generate_text(
        prompt=prompt,
        image=img_b64  # Vision model accepts images
    )
    
    return response