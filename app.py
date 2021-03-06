import io
import numpy as np
import tensorflow as tf
from PIL import Image
from flask import Flask, jsonify, request

model = tf.keras.models.load_model('model/retinal-oct.h5')

def prepare_image(img):
    img = Image.open(io.BytesIO(img))
    img = img.resize((150, 150))
    img = np.expand_dims(img, 0)
    img = np.stack((img,)*3, axis=-1)
    
    return img


def predict_result(img):
    Y_pred = model.predict(img)
    return np.argmax(Y_pred, axis=1)


app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def infer_image():
    if 'file' not in request.files:
        return "Please try again. The Image doesn't exist"
    
    file = request.files.get('file')

    if not file:
        return

    img_bytes = file.read()
    img = prepare_image(img_bytes)
    return jsonify(prediction=int(predict_result(img)))
    

@app.route('/', methods=['GET'])
def index():
    return 'Machine Learning Inference'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
