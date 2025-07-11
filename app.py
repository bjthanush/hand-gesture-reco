from flask import Flask, render_template, request, jsonify
from transformers import AutoModelForImageClassification, AutoImageProcessor
from PIL import Image
import torch
import io
import re
import base64

app = Flask(__name__)

# Load model + processor
model_dir = "./model"
model = AutoModelForImageClassification.from_pretrained(model_dir)
processor = AutoImageProcessor.from_pretrained(model_dir)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    img_data = data['image']

    # Convert base64 -> PIL Image
    img_str = re.search(r'base64,(.*)', img_data).group(1)
    img_bytes = base64.b64decode(img_str)
    img = Image.open(io.BytesIO(img_bytes)).convert('RGB')

    # Predict
    inputs = processor(images=img, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        pred_idx = logits.argmax(-1).item()
        pred_label = model.config.id2label[pred_idx]

    return jsonify({'prediction': pred_label})

if __name__ == "__main__":
    app.run(debug=True)
