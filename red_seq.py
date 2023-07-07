import os
import requests
import json
from datetime import datetime
from configparser import ConfigParser

LOG_FILENAME = "red_seq.log"

config = ConfigParser()
config.read("config.ini")

# Access configuration values
PROJECT = config.get('RESOURCES', 'project_id')
TRACKER = config.get('RESOURCES', 'tracker_id')
SUBJECT = config.get('RESOURCES', 'subject')
VALUE = config.get('API', 'value')
URL = config.get('URL', 'url')
UPLOAD_URL = config.get('URL', 'upload_url')
PATH = config.get('PATH', 'path')
DATETIMENOW = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
url = URL.split("/")

data = {
    "issue": {
        "project_id": PROJECT,
        "tracker_id": TRACKER,
        "subject": SUBJECT,  # {date.today()
        "uploads": [
        ]
    }
}

def write_logs(request, respond, error):
    if respond and request:
        if os.path.exists(LOG_FILENAME):
            with open(LOG_FILENAME, "a") as file:
                file.write(f"\n{DATETIMENOW} REQUEST {request}")
                file.write(f"\n{DATETIMENOW} RESPOND {respond}")
        else:
            with open("red_seq.log", "w") as file:
                file.write(f"{DATETIMENOW} REQUEST {request}\n")
                file.write(f"{DATETIMENOW} RESPOND {respond}")
    else:
        if os.path.exists(LOG_FILENAME):
            with open(LOG_FILENAME, "a") as file:
                file.write(f"\n{DATETIMENOW} ERROR {error}")
        else:
            with open(LOG_FILENAME, "w") as file:
                file.write(f"{DATETIMENOW} ERROR {error}")

try:
    request = requests.get(f"{url[0]}//{url[2]}", timeout=3)
    if request.status_code == 200:
        for filename in os.listdir(PATH):
            if os.path.isfile(os.path.join(PATH, filename)):
                with open(f"{PATH}{filename}", "rb") as file:
                    files = {"filename": file}
                    headers = {"Content-Type": "application/octet-stream", "X-Redmine-API-Key": VALUE}
                    response = requests.post(UPLOAD_URL, files=files, headers=headers)
                if response.status_code == 201:
                    attachment_token = response.json().get("upload", {}).get("token")
                # print(f"File uploaded successfully. Token: {attachment_token}")
                    data["issue"]["uploads"].append({"token": attachment_token, "filename": filename, "content_type": "text/plain"})
            # else:
                # write_logs("","", f"File upload failed. Error: {response.status_code}")
        headers = {"Content-Type": "application/json", "X-Redmine-API-Ke": VALUE}
        request = requests.post(URL, headers=headers, data=json.dumps(data))
        write_logs(json.dumps(data), request.json(), "No error")
    # else:
        # write_logs("", "", f"Error: {request.status_code}")
except FileNotFoundError as e:
    write_logs("", "", f"{e}")
except requests.exceptions.RequestException as e:
    write_logs("", "", f"Failed to connect to the server: {e}")
