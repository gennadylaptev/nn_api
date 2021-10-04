import pytest
from nn_api.service_layer.inference import Inferer


@pytest.fixture
def inferer():
    return Inferer()


