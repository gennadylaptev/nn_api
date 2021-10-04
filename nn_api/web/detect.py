from flask import Blueprint, flash, request


bp = Blueprint('detect', __name__, url_prefix='/')


@bp.route('/detect', methods=['GET', 'POST'])
def detect():
    
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
