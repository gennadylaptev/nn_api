import os
from flask import Flask, request 
from nn_api.service_layer import inference


# define an app factory
def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)
    inferer = inference.Inferer()

    # store an `Inferer` instance in app config
    app.config['inferer'] = inferer
    
    #if test_config is None:
    #    app.config.from_pyfile('config.py', silent=True)
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # main logic of handling object detection requests
    from . import detect
    app.register_blueprint(detect.bp)

    return app

