import requests
import json
url = 'http://127.0.0.1:8000/rest-auth/register/'
header = {'Content-type':'application/json'}
payload = {"username":"xxxmzhmmmxxxjun","password":"123456","email":"fa@fl.com","first_name":"afdsfa","last_name":"fadfadfa"}
# payload1 = {"username":"zhjun","password":"123456","email":"fa@fl.com","newsletter_subscribe":"false"}
r = requests.post(url,data=json.dumps(payload),headers=header)
r.encoding = 'gbk'
# print r.encoding
# print r.text
# print r.content
print r.json()

