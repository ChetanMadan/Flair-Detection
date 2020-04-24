import requests

URL = "https://redditflairdetect.herokuapp.com/automated_testing"

files = {'file': open('file.txt', 'r')}
r = requests.post(URL, files=files, data={})
print(str(r.text))

#print(requests.Request('POST', URL, files=files).prepare().body.decode('ascii'))
#r = requests.post(url = URL, data = params)

