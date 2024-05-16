import requests

url = 'http://127.0.0.1:5000/upload-image'
file_path = './images/noisy.png'

with open(file_path, 'rb') as file:
    files = {'file': file}
    response = requests.post(url, files=files)

if response.status_code == 200:
    # Save the image returned by the API
    with open('output.png', 'wb') as f:
        f.write(response.content)
    print("Image received and saved as output.png")
else:
    print(f"Failed to receive image. Status code: {response.status_code}, Error: {response.json()}")
