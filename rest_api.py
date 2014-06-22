#!/usr/bin/python
import requests
import json
import sys
url1 = 'http://127.0.0.1:8000/rest-auth/register/'
url = 'http://135.252.37.114:9999/rest-auth/register/'
url3 = 'http://135.252.37.114:9999/rest-auth/logout/'
url4 = 'http://115.28.79.151:8081/dangjian/laoshanparty/v1/register/'
header = {'Content-type':'application/json'}
payload = {"username":"mzhmmm222xxxjun","password":"123456","email":"fa@fl.com","first_name":"afdsfa","last_name":"fadfadfa"}
payload2 = {"username":"mzhmmm222xxxjun","password":"123456"}
# payload1 = {"username":"zhjun","password":"123456","email":"fa@fl.com","newsletter_subscribe":"false"}
r = requests.post(url4,data=json.dumps(payload),headers=header)
print r.headers
# r = requests.get(url3,headers=header)
print r.encoding
print r.text
# print r.content
print r.json()
print r.status_code
