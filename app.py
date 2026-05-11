from flask import Flask
from flask import render_template
from flask import request
import os

from utils.prediction import predict_disease
from utils.recommendation import get_recommendation

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():

    file = request.files['image']

    if file:

        filepath = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )

        file.save(filepath)

        disease, confidence = predict_disease(filepath)

        info = get_recommendation(disease)

        if confidence >= 90:
            severity = 'High'

        elif confidence >= 70:
            severity = 'Medium'

        else:
            severity = 'Low'

        return render_template(
            'result.html',
            disease=disease,
            confidence=confidence,
            severity=severity,
            cause=info['cause'],
            symptoms=info['symptoms'],
            treatment=info['treatment'],
            prevention=info['prevention'],
            image_path=filepath
        )


if __name__ == '__main__':
    app.run(debug=True)
