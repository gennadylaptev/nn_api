import io
import torch
import torchvision
from torchvision import transforms
#from torchvision.transforms import functional as F
import numpy as np
from PIL import Image


class Inferer:

    # transformation with normalization to [0.0, 1.0]
    pil2tensor = transforms.ToTensor()

    def __init__(self):
        # hardcoded model
        self.model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
        self.model = self.model.eval()
    
    @staticmethod
    def jsonify_output(output):
        """ transforms an output from the torchvision model to a JSONable dict """
        res = {}
        for k, v in output.items():
            if isinstance(v, torch.Tensor):
                v = v.tolist()
            res[k] = v
        return res

    @staticmethod
    def prepare_image(file_obj: io.IOBase):
        """ return: normalized tensor """
        img = Image.open(file_obj)
        return Inferer.pil2tensor(img.convert('RGB'))

    def infer(self, img: io.IOBase):
        # transform input to tensor
        img = self.prepare_image(img)
        
        # run NN model
        with torch.no_grad():
            # take the first element from the resulting list
            output = self.model([img])[0]

        res = self.jsonify_output(output)
        return res
