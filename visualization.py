import io

import torch
from torchvision.utils import draw_bounding_boxes, save_image

from typing import Dict

def prepare_image_bb(img: torch.Tensor, model_output: Dict[str, torch.Tensor]):
    
    # TODO: error when `img` is not tensor
    if not isinstance(img, torch.Tensor):
        pass

    if not isinstance(model_output, dict):
        model_output = {}

    #model_output = model_output.get('object_detection', {})
    boxes = model_output.get('boxes', torch.tensor([]))
    
    colors = ['red' for _ in range(len(boxes))]

    img_bb = draw_bounding_boxes(img, boxes, colors=colors, width=4)

    with io.BytesIO() as stream:
        save_image(img_bb / 256, stream, width=4, colors=['red'], format='JPEG')
        res = stream.getvalue()
    
    return res

