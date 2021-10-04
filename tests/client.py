import requests
from tests import prepare_image_as_list

# A http-client for testing purposes
# It just sends a picture (in json format) to the server


def run_client(url='http://127.0.0.1:5000/infer/json', port=5000):

    img_list = prepare_image_as_list()
    
    # form POST request data
    data = {'image': img_list}
    response = requests.post(url, json=data)
    
    # raise exception if we made a bad request
    response.raise_for_status()

    print(response)
    print(response.json())


if __name__ == "__main__":
    run_client()
