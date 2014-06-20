#!/usr/bin/python
import requests
import json
import sys
url1 = 'http://127.0.0.1:8000/rest-auth/register/'
url = 'http://135.252.37.114:9999/rest-auth/register/'
url3 = 'http://135.252.37.114:9999/rest-auth/logout/'
header = {'Content-type':'application/json'}
payload = {"username":"mzhmmm222xxxjun","password":"123456","email":"fa@fl.com","first_name":"afdsfa","last_name":"fadfadfa"}
payload2 = {"username":"mzhmmm222xxxjun","password":"123456"}
# payload1 = {"username":"zhjun","password":"123456","email":"fa@fl.com","newsletter_subscribe":"false"}
r = requests.post(url,data=json.dumps(payload),headers=header)
print r.headers
# r = requests.get(url3,headers=header)
print r.encoding
print r.text
# print r.content
print r.json()
print r.status_code

# def rest(argv=None):
#     print argv
#     method = argv[1]


# class rest():
#     def __init__(self,*args):
#         method = 'GET'
#         url = 'http://135.252.37.114:9999'
#         appendix = ''
#         payload = {}
#         header = ''


#     def do_request(self):
#         if self.method == 'GET':
#             request.GET(self.url,data=json.dumps(self.payload),headers = self.header)
#         else:
#             request.POST(self.url,data=json.dumps(self.payload),headers = self.header)

    
# if __name__ == '__main__':
#     rest(sys.argv)


