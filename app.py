from flask import Flask, request, jsonify, send_file
from test_denoise import img2tensor, predict_single_image
from basicsr.models import create_model
from basicsr.utils.options import parse
from basicsr.utils import imwrite
from datetime import datetime
import numpy as np
import os
from PIL import Image


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

opt_path = 'options/NAFNet-width32.yml'
opt = parse(opt_path, is_train=False)
opt['dist'] = False
NAFNet = create_model(opt)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/upload-image', methods=['POST'])
def upload_image():

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        file_extension = os.path.splitext(file.filename)[1].lower()
        # Read the image file into a PIL Image
        image = Image.open(file.stream)

        # Convert the image to a NumPy array
        image_np = np.array(image)

        # Convert the NumPy array to a tensor
        tensorImg = img2tensor(image_np)

        # Predict using the model
        result_img = predict_single_image(NAFNet, tensorImg)
        now = datetime.now()
        timestamp_str = now.strftime("%Y%m%d_%H%M%S")
        img_path = f"images/{timestamp_str}_image{file_extension}"
        imwrite(result_img, img_path)

        # Send the file
        return send_file(img_path,  mimetype=f'image/{file_extension[1:]}')





if __name__ == '__main__':
    app.run()
