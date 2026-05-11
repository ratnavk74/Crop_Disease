from flask import Flask, render_template, request
import tensorflow as tf
import numpy as np
import cv2
import os
from disease_info import DISEASE_INFO

app = Flask(__name__)

# Load trained model
model = tf.keras.models.load_model('crop_disease_model.h5')

# Classes
classes = [
    'Maize_Blight',
    'Maize_Common_Rust',
    'Maize_Healthy',
    'Wheat_Healthy',
    'Wheat_Rust',
    'Wheat_Septoria'
]

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Preprocess image

def preprocess_image(path):
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (224, 224))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    return img

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():

    file = request.files['image']

    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        processed_image = preprocess_image(filepath)

        prediction = model.predict(processed_image)
        predicted_class = classes[np.argmax(prediction)]
        confidence = round(np.max(prediction) * 100, 2)

        info = DISEASE_INFO[predicted_class]

        return render_template(
            'result.html',
            disease=predicted_class,
            confidence=confidence,
            cause=info['cause'],
            symptoms=info['symptoms'],
            treatment=info['treatment'],
            prevention=info['prevention'],
            image_path=filepath
    app.run(debug=True)
