import requests

files = {"upload_file": open("./testing_scripts/publisher_decline_list.xlsx", "rb")}
r = requests.put(
    "http://127.0.0.1:8000/upload/publisher_decline_list.xlsx", files=files
)

print(r.status_code)
assert r.status_code == 204
