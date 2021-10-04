import requests

# A http-client for testing purposes
# It just sends a picture (in json format) to the server


def run_client(url='http://127.0.0.1:5000/detect', port=5000, image_file='dogs.jpg'):
    
    with open(image_file, 'rb') as f:
        img = f.read()
    
    # form POST request data
    data = {'file': img}
    response = requests.post(url, files=data)
    
    # raise exception if we made a bad request
    #response.raise_for_status()

    print(response)
    print(response.json())


if __name__ == "__main__":
    run_client()
