import os
from PIL import Image
from flask import Flask, request, flash, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

from inferer import Inferer


# basic hardcoded config
APP_ROOT = os.getenv('APP_ROOT', '/infer')
HOST = '0.0.0.0'
PORT_NUNMBER = int(os.getenv('PORT_NUMBER', 8080))
ALLOWED_EXTENSIONS = {'jpeg', 'jpg', 'png', 'gif'}
UPLOAD_FOLDER = './user_data'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
inferer = Inferer() 


@app.route('/hello')
def hello():
    return 'Hello! Send some jsons with `image` field to `/infer`'


# just get an image from request json and execute Inferer
@app.route('/infer/json', methods=['GET', 'POST'])
def infer():
    
    if request.method == 'GET':
        return 'Please send json via POST request'

    data = request.json
    image = data['image']
    res = inferer.infer(image)
    
    return res


def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/infer/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':

        if 'file' not in request.files:
            flash('No file part!')
            return redirect(request.url)

        file = request.files['file']

        # If user doesn't send a file, the browser submits empty file
        if file.filename == '':
            flash('No selected file!')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            
            # make filename secure and save it to the server
            filename = secure_filename(file.filename)

            # send this file to the NN
            res = inferer.infer(file.stream, input_type='file')
            return res

            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            # after receiving a file from the user
            # redirect to a view that downloads a file
            # and shows it to the user
            
            #return redirect(url_for('download_file', name=filename))

    # show html page with upload form
    return '''
    <!doctype html>
    <title>Upload picture for object detection</title>
    <h1>Upload picture for object detection</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value="Upload">
    </form>
    '''


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config['UPLOAD_FOLDER'], name)


if __name__ == '__main__':
    app.run(host=HOST, port=PORT_NUMBER)

