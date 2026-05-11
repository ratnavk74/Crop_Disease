import tensorflow as tf
import numpy as np
from utils.preprocess import preprocess_image

model = tf.keras.models.load_model(
    'models/advanced_crop_disease_model.h5'
)

classes = [
    'Maize_Blight',
    'Maize_Common_Rust',
    'Maize_Healthy',
    'Wheat_Healthy',
    'Wheat_Rust',
    'Wheat_Septoria'
]


def predict_disease(image_path):

    processed_image = preprocess_image(image_path)

    prediction = model.predict(processed_image)

    predicted_class = classes[np.argmax(prediction)]

    confidence = round(np.max(prediction) * 100, 2)

    return predicted_class, confidence
