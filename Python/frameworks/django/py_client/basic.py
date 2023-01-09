import requests

endpoint = "http://127.0.0.1:8000/api/"

get_response = requests.get(endpoint, json={"foo": "boo"})
print(get_response.status_code)
print(get_response.text.splitlines()[0]) 