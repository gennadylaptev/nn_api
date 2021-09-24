from PIL import Image
import numpy as np
from inferer import Inferer

img_path = './test_imgs/dogs.jpg'


def prepare_image_as_list():

    img = Image.open(img_path).convert('RGB')
    img_list = np.asarray(img).tolist()     
    
    return img_list


def test_inferer():
    x = prepare_image_as_list()
    inferer = Inferer()

    out = inferer.infer(x)

    print(out)


def test_inference_on_uploaded_image():
    inferer = Inferer()

    model_output = inferer.infer(img_path, input_type='file')
    

def test_visualize_bb():
    pass


if __name__ == '__main__':
    #test_inferer()

