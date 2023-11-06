import os
import sys
import json
import urllib.request
from dotenv import load_dotenv

load_dotenv()

NAVER_CLIENT_ID = os.getenv('NAVER_CLIENT_ID')
NAVER_CLIENT_SECRET = os.getenv('NAVER_CLIENT_SECRET')

encText = urllib.parse.quote('여행')
dateText = urllib.parse.quote('date')
url = 'https://openapi.naver.com/v1/search/blog?query=' + encText + '&display=100&sort=' + dateText

request = urllib.request.Request(url)
request.add_header('X-Naver-Client-Id', NAVER_CLIENT_ID)
request.add_header('X-Naver-Client-Secret', NAVER_CLIENT_SECRET)

res = urllib.request.urlopen(request)
rescode = res.getcode()

if(rescode == 200):
    response_body = res.read()
    decoded_data = response_body.decode('utf-8')
    json_data = json.loads(decoded_data)
    print(json_data)
    items = json_data['items']
    title = []
    postdate = []
    for item in items:
        title.append(item['title'])
        postdate.append(item['postdate'])
    print(title)
    print(postdate)
else:
    print('Error Code:' + rescode)