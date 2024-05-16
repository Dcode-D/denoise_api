from flask import Flask, request, jsonify, send_file
from test_denoise import img2tensor, predict_single_image
from basicsr.models import create_model
from basicsr.utils.options import parse
import tempfile
import numpy as np
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
        # Read the image file into a PIL Image
        image = Image.open(file.stream)

        # Convert the image to a NumPy array
        image_np = np.array(image)

        # Convert the NumPy array to a tensor
        tensorImg = img2tensor(image_np)

        # Predict using the model
        result_tensor = predict_single_image(NAFNet, tensorImg)

        # Check if result_tensor is indeed a tensor
        # if hasattr(result_tensor, 'detach'):
        #     # Convert the tensor back to a NumPy array
        #     result_image_np = result_tensor.squeeze().detach().cpu().numpy()
        # else:
        #     result_image_np = result_tensor.squeeze()
        result_image_np = result_tensor.squeeze()
        # Normalize image data
        result_image_np_normalized = (result_image_np - np.min(result_image_np)) / (np.max(result_image_np) - np.min(result_image_np))

        # Scale to [0, 255] and convert to uint8
        result_image_np_uint8 = (result_image_np_normalized * 255).astype(np.uint8)

        # Normalize and convert to uint8
        if result_image_np_uint8.ndim == 2:
            result_image_pil = Image.fromarray(result_image_np_uint8, mode='L')
        else:
            result_image_pil = Image.fromarray(result_image_np_uint8, mode='RGB')


# Save the result image to a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        result_image_pil.save(temp_file, format='PNG')
        temp_file.close()

        # Send the file
        return send_file(temp_file.name, mimetype='image/png')





if __name__ == '__main__':
    app.run()
