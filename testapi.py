import requests

filename = "images/dog.jpg"
files = {"my_file": (filename, open(filename, "rb"))}

response = requests.post(
    "http://127.0.0.1:8000/file",
    files=files,
)
print(response.json())