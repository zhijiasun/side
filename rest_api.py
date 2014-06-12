import requests
r = requests.get("http://127.0.0.1:8000/epm/pioneer",params={"username":"jasonsun","password":"123456"})
print r.json()

