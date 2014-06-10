import requests
r = requests.get("http://127.0.0.1:8000/member/")
print r.text
print r.json()
print r.content

