import requests

headers = {"X-Redmine-API-Key": "9751d3c925b7bece550d2ba310aa1d3667295655"}
URL = "http://192.168.154.128/issues/34233.json"

request = requests.get(URL, headers=headers)

if request.status_code == 200:
    print(request.json())
else:
    print(f"Error: {request.status_code}")
