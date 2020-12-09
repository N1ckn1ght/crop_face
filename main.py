import http.client
import urllib.request
import urllib.parse
import urllib.error
import json
from PIL import Image

uri = '/face/v1.0/detect?returnFaceId=true'
headers = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': 'INSERT_YOUR_TOKEN_HERE',
}

path = '.\\example\\snapshot.jpg'
path_output = '.\\example\\crop'

with open( path, 'rb' ) as f:
    body = f.read()

try:
    conn = http.client.HTTPSConnection('westeurope.api.cognitive.microsoft.com')
    conn.request('POST', uri, body, headers)
    response = conn.getresponse()
    data = response.read().decode('utf-8')
    data = json.loads(data)
    conn.close()

    _id = 0
    for i in data:
        rec = i['faceRectangle']
        area = (rec['left'], rec['top'],
                rec['left'] + rec['width'], rec['top'] + rec['height'])
        img = Image.open(path)
        img = img.crop(area)
        img.save(path_output + str(_id) + '.jpg')
        _id += 1

except Exception as e:
    print('[Errno {0}] {1}'.format(e.errno, e.strerror))
