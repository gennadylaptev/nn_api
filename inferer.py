import torch
import torchvision
from torchvision import transforms
import numpy as np


class Inferer:
    def __init__(self):
        # hardcoded model
        self.model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
        self.model = self.model.eval()
        self.pil2tensor = transforms.ToTensor()
    
    @staticmethod
    def _jsonify_output(output):
        res = {}
        for k, v in output.items():
            if isinstance(v, torch.Tensor) or isintance(v. np.ndarray):
                v = v.tolist()

            res[k] = v
        return res

    @staticmethod
    def jsonify_batch_output(batch_output):
        return {'object_detection': [Inferer._jsonify_output(x) for x in batch_output]}

    def infer(self, img_list):
        # we pass an image as a python list that was extracted
        # from request json
        img = self.pil2tensor(np.asarray(img_list, dtype=np.float32))
        
        with torch.no_grad():
            res = self.jsonify_batch_output(self.model([img]))

        return res
