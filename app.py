import os
import io
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template,jsonify,json
from werkzeug.utils import secure_filename
from utils.detect_text_aws import  get_text


UPLOAD_FOLDER = 'static/uploads/'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


@app.route('/')
def start_page():
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        statement='No file part'
        return render_template('index.html',statement=statement)
    file = request.files['file']
    if file.filename == '':
        statement='No image selected for uploading'
        return render_template('index.html', statement=statement)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        response, res_img, res_response, statement = get_text(filename)
        if statement == "success":
            return render_template('index.html', jsonfile=json.dumps(response, indent=4),
                                   result_json_response=res_response, filename=res_img, result_image=res_img,
                                   statement=statement)
        else:
            return render_template('index.html', statement=statement)
    else:
        statement='Allowed image types are -> png, jpg, jpeg'
        return render_template('index.html', statement=statement)


@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route('/display_result_image/<filename>')
def display_result_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='result/' + filename), code=301)


@app.after_request
def add_header(response):
    response.headers['Pragma'] = 'no-cache'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Expires'] = '0'
    return response


if __name__ == '__main__':
    app.run(port=5001)