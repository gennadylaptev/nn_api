import os
from PIL import Image
from flask import Flask, request
from inferer import Inferer


app = Flask(__name__)


# basic hardcoded config
APP_ROOT = os.getenv('APP_ROOT', '/infer')
HOST = '0.0.0.0'
PORT_NUNMBER = int(os.getenv('PORT_NUMBER', 8080))


inferer = Inferer() 

@app.route('/hello')
def hello():
    return 'Hello! Send some jsons with `image` field to `/infer`'


# just get an image from request json and execute Inferer
@app.route('/infer', methods=['GET', 'POST'])
def infer():
    
    if request.method == 'GET':
        return 'Please send json via POST request'

    data = request.json
    image = data['image']
    res = inferer.infer(image)
    
    return res


if __name__ == '__main__':
    app.run(host=HOST, port=PORT_NUMBER)

