import os
import sys
import json
import urllib.request
from dotenv import load_dotenv

load_dotenv()

NAVER_CLIENT_ID = os.getenv('NAVER_CLIENT_ID')
NAVER_CLIENT_SECRET = os.getenv('NAVER_CLIENT_SECRET')

encText = urllib.parse.quote('여행')
url = 'https://openapi.naver.com/v1/search/blog?query=' + encText

request = urllib.request.Request(url)
request.add_header('X-Naver-Client-Id', NAVER_CLIENT_ID)
request.add_header('X-Naver-Client-Secret', NAVER_CLIENT_SECRET)

res = urllib.request.urlopen(request)
rescode = res.getcode()

if(rescode == 200):
    response_body = res.read()
    decoded_data = response_body.decode('utf-8')
    json_data = json.loads(decoded_data)
    items = json_data['items']
    title = []
    for item in items:
        title.append(item['title'])
    print(title)
else:
    print('Error Code:' + rescode)
#안녕하세요
#안녕하세요2
