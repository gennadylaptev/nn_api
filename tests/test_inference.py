import pytest
from reprlib import repr

import logging
#logging.basicConfig(level=logging.DEBUG)
#logger = logging.getLogger()
#from loguru import logger


test_image_path = 'dogs.jpg'


def test_inference(inferer):
    with open(test_image_path, 'rb') as img:
        res = inferer.infer(img)
    
    #caplog.set_level(logging.INFO)
    logging.getLogger().info(f'Model output: {repr(res)}')

    assert isinstance(res, dict)
    assert 'boxes' in res
    assert 'labels' in res

    return res


