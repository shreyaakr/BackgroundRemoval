import cv2
import os
from rembg.bg import remove as advanced_remove
from PIL import Image
from werkzeug.utils import secure_filename
from flask import Flask, request, render_template

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'webp'])

if 'static' not in os.listdir('.'):
    os.mkdir('static')

if 'uploads' not in os.listdir('static/'):
    os.mkdir('static/uploads')

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "secret key"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def remove_background(input_path, output_path):
    input_image = Image.open(input_path)
    output_image = advanced_remove(input_image)
    output_image.save(output_path)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/remback', methods=['POST'])
def remback():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        rembg_img_name = filename.split('.')[0] + "_rembg.png"
        rembg_img_path = os.path.join(app.config['UPLOAD_FOLDER'], rembg_img_name)
        remove_background(file_path, rembg_img_path)

        return render_template('home.html', org_img_name=filename, rembg_img_name=rembg_img_name)

if __name__ == '_main_':
    app.run(debug=True)