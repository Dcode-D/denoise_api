import requests

url = 'http://127.0.0.1:5000/upload-image'
file_path = './images/cat.jpg'

with open(file_path, 'rb') as file:
    files = {'file': file}
    response = requests.post(url, files=files)

print(response.json())