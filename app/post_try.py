import requests

URL = "http://127.0.0.1:5000/automated_testing"

files = {'file': open('file.txt', 'r')}
r = requests.post(URL, files=files, data={})
print(str(r.text))

#print(requests.Request('POST', URL, files=files).prepare().body.decode('ascii'))
#r = requests.post(url = URL, data = params)

