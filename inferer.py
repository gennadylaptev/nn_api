import torch
import torchvision
from torchvision import transforms
from torchvision.transforms import functional as F
import numpy as np

from PIL import Image

from visualization import prepare_image_bb

class Inferer:

    # transformation with normalization to [0.0, 1.0]
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
        """ return: normalized, unnormalized tensors """
        img = Image.open(file_obj)

        return Inferer.pil2tensor(img.convert('RGB')), F.pil_to_tensor(img)

    def infer(self, img, input_type='json', output_type='json'):
        # transform input to tensor
        if input_type == 'json': 
            img = self._prepare_json(img)
        elif input_type == 'file':
            img, img_unnorm = self._prepare_file(img)
        
        # run NN model
        with torch.no_grad():
            # take the first element from the resulting list
            output = self.model([img])[0]

        if output_type == 'json':
            res = self.jsonify_batch_output(output)
        if output_type == 'image':
            res = prepare_image_bb(img_unnorm, output)

        return res
