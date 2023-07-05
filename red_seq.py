import requests
import json

HEADER = {"X-Redmine-API-Key": "9751d3c925b7bece550d2ba310aa1d3667295655"}
URL = "http://192.168.154.128/issues/34233.json"

data = {
	"issue": {
		"project_id": 118,
		"tracker_id": 88,
		"subject": "Hello world"
	}
}

DATA = json.dumps(data)

print(DATA)



# request = requests.get(URL, headers=HEADER)

# if request.status_code == 200:
#     print(request.json())
# else:
#     print(f"Error: {request.status_code}")
