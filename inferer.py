import torch
import torchvision
from torchvision import transforms
import numpy as np

from PIL import Image


class Inferer:

    pil2tensor = transforms.ToTensor()

    def __init__(self):
        # hardcoded model
        self.model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
        self.model = self.model.eval()
    
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
    
    @staticmethod
    def _prepare_json(img):
        return Inferer.pil2tensor(np.asarray(img, dtype=np.float32))
    
    @staticmethod
    def _prepare_file(file_obj):
        return Inferer.pil2tensor(Image.open(file_obj).convert('RGB'))

    def infer(self, img, input_type='json'):
        # transform input to tensor
        if input_type == 'json': 
            img = self._prepare_json(img)
        elif input_type == 'file':
            img = self._prepare_file(img)
        
        # run NN model
        with torch.no_grad():
            res = self.jsonify_batch_output(self.model([img]))

        return res
