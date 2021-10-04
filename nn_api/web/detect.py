from flask import Blueprint, flash, request, current_app
from nn_api.service_layer import files


bp = Blueprint('detect', __name__, url_prefix='/')


@bp.route('/detect', methods=['GET', 'POST'])
def detect():
    
    inferer = current_app.config['inferer']

    if request.method == 'GET':
        return 'Please send an image via POST request'
    
    # get the file from the request
    f = request.files['file']

    # process the file
    try:
        img = files.process_file(f)
    except (files.EmptyFile, files.ExtensionNotAllowed, files.NoFilePart) as e:
        return {'message': str(e)}, 400

    # send file to the model
    output = inferer.infer(img)
    
    return output, 200
