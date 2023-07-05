import requests
import json
from datetime import date


HEADER = {
    "Content-Type": "application/json",
    "X-Redmine-API-Key": "9751d3c925b7bece550d2ba310aa1d3667295655"
}
URL = "http://192.168.154.128/issues.json"
TODAY = date.today()

data = {
	"issue": {
		"project_id": 118, # Test project for me
		"tracker_id": 88, # Tracker id 
		"subject": f"VW380 / Нові зварні вузли /  {TODAY}"
	}
}
DATA = json.dumps(data)

request = requests.post(URL, headers=HEADER, data=DATA)
if request.status_code == 201:
    print(request.json())
else:
    print(f"Error: {request.status_code}")
