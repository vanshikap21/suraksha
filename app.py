from flask import Flask, request, jsonify, render_template
import cv2
import numpy as np
import joblib
from PIL import Image
import io
import datetime
from flask_cors import CORS
import os

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

model = joblib.load("anemia_rf_model.pkl")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict-image", methods=["POST", "OPTIONS"])
def predict_image():
    if request.method == "OPTIONS":
        return '', 204

    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['image']
    image_stream = file.read()
    pil_image = Image.open(io.BytesIO(image_stream)).convert("RGB")
    image = np.array(pil_image)

    red = np.mean(image[:, :, 0]) / 255 * 100
    green = np.mean(image[:, :, 1]) / 255 * 100
    blue = np.mean(image[:, :, 2]) / 255 * 100
    hb = 10.5

    features = np.array([[red, green, blue, hb]])
    prediction = model.predict(features)
    proba = model.predict_proba(features)[0]
    confidence = round(max(proba) * 100, 2)

    label = "anemic" if prediction[0] == 1 else "not anemic"

    return jsonify({
        "result": {
            "label": label,
            "timestamp": datetime.datetime.now().isoformat(),
            "hemoglobin": hb,
            "confidence": confidence
        }
    })

@app.route('/test-css')
def test_css():
    return '<link rel="stylesheet" href="/static/styles.css"><div class="screen">CSS?</div>'

# Let Render assign port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
