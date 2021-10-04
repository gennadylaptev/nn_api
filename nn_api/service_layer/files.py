from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'jpeg', 'jpg', 'png', 'gif'}


class NoFilePart(Exception):
    pass


class EmptyFile(Exception):
    pass


class ExtensionNotAllowed(Exception):
    pass


def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def _check_file(f):

    """ f: `request.files['file']` from Flask web app """
    
    if not f:
        raise NoFilePart('No file part in the request')

    if f.filename == '':
        raise EmptyFile('No file has been sent')
    
    if f.filename not in ALLOWED_EXTENSIONS:
        raise ExtensionNotAllowed('This file extension is not allowed')


def process_file(f):
    
    """ f: werkzeug.datastructures.FileStorage
        return: file object
    """

    _check_file(f)
    
    # return the file object
    return f.stream
