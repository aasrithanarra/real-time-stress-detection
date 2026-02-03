from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np

from emotion_stress import analyze_frame

app = Flask(__name__)

# -----------------------------
# Home page
# -----------------------------
@app.route("/")
def index():
    return render_template("index.html")

# -----------------------------
# REST API for stress analysis
# -----------------------------
@app.route("/analyze", methods=["POST"])
def analyze():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]

    # Convert uploaded image to OpenCV format
    img_bytes = np.frombuffer(file.read(), np.uint8)
    frame = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)

    if frame is None:
        return jsonify({"error": "Invalid image"}), 400

    result = analyze_frame(frame)

    if result is None:
        return jsonify({"error": "No face detected"}), 200

    return jsonify(result), 200


if __name__ == "__main__":
    app.run(debug=True)