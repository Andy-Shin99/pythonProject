# from pytrends.request import TrendReq
#
# pytrends = TrendReq(hl='ko', tz=540)
#
# keyword = ['여행'] # cat num = 67
# pytrends.build_payload(keyword, cat=67, timeframe='2023-01-01 2023-11-06', geo='KR')
# data = pytrends.interest_over_time()
#
# print(data)


### pytrend 429 error 때문에 다른 코드,,
import json
import urllib.parse
from datetime import datetime, timedelta
from curl_cffi import requests
import time

def build_payload(keywords, timeframe='now 7-d', geo='US'):
    token_payload = {
        'hl': 'en-US',
        'tz': '0',
        'req': {
            'comparisonItem': [{'keyword': keyword, 'time': timeframe, 'geo': geo} for keyword in keywords],
            'category': 0,
            'property': ''
        }
    }
    token_payload['req'] = json.dumps(token_payload['req'])
    return token_payload

def convert_to_desired_format(raw_data):
    trend_data = {}
    for entry in raw_data['default']['timelineData']:
        timestamp = int(entry['time'])
        date_time_str = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        value = entry['value'][0]
        trend_data[date_time_str] = value
    return trend_data

# Cookies
def get_google_cookies(impersonate_version='chrome110'):
    with requests.Session() as session:
        session.get("https://www.google.com", impersonate=impersonate_version)
        return session.cookies

def fetch_trends_data(keywords, days_ago=7, geo='US', hl='en-US', max_retries=5, browser_version='chrome110', browser_switch_retries=2):
    browser_versions = ['chrome110', 'edge101', 'chrome107', 'chrome104', 'chrome100', 'chrome101', 'chrome99']
    current_browser_version_index = browser_versions.index(browser_version)
    cookies = get_google_cookies(impersonate_version=browser_versions[current_browser_version_index])

    for browser_retry in range(browser_switch_retries + 1):
        data_fetched = False
        with requests.Session() as s:
            # phase 1: token
            for retry in range(max_retries):
                time.sleep(2)
                token_payload = build_payload(keywords)
                url = 'https://trends.google.com/trends/api/explore'
                params = urllib.parse.urlencode(token_payload)
                full_url = f"{url}?{params}"
                response = s.get(full_url, impersonate=browser_versions[current_browser_version_index], cookies=cookies)
                if response.status_code == 200:
                    content = response.text[4:]
                    try:
                        data = json.loads(content)
                        widgets = data['widgets']
                        tokens = {}
                        request = {}
                        for widget in widgets:
                            if widget['id'] == 'TIMESERIES':
                                tokens['timeseries'] = widget['token']
                                request['timeseries'] = widget['request']
                        break
                    except json.JSONDecodeError:
                        print(f"Failed to decode JSON while fetching token, retrying {retry + 1}/{max_retries}")
                else:
                    print(f"Error {response.status_code} while fetching token, retrying {retry + 1}/{max_retries}")
            else:
                print(f"Exceeded maximum retry attempts ({max_retries}) while fetching token. Exiting...")
                return None

            for retry in range(max_retries):
                time.sleep(5)
                req_string = json.dumps(request['timeseries'], separators=(',', ':'))
                encoded_req = urllib.parse.quote(req_string, safe=':,+')
                url = f"https://trends.google.com/trends/api/widgetdata/multiline?hl={hl}&tz=0&req={encoded_req}&token={tokens['timeseries']}&tz=0"
                response = s.get(url, impersonate=browser_versions[current_browser_version_index], cookies=cookies)
                if response.status_code == 200:
                    content = response.text[5:]
                    try:
                        raw_data = json.loads(content)
                        trend_data = convert_to_desired_format(raw_data)
                        data_fetched = True
                        return trend_data
                    except json.JSONDecodeError:
                        print(f"Failed to decode JSON while fetching trends data, retrying {retry + 1}/{max_retries}")
                else:
                    print(f"Error {response.status_code} while fetching trends data, retrying {retry + 1}/{max_retries}")
            else:
                print(f"Exceeded maximum retry attempts ({max_retries}) while fetching trends data.")

        # 브라우저 변경
        if not data_fetched and browser_retry < browser_switch_retries:
            time.sleep(5)
            current_browser_version_index = (current_browser_version_index + 1) % len(browser_versions)
            print(f"Switching browser version to {browser_versions[current_browser_version_index]} and retrying...")

    print(f"Exceeded maximum browser switch attempts ({browser_switch_retries}). Exiting...")
    return None

# 사용 예시
keywords = ["여행"]
trends_data = fetch_trends_data(keywords)
print(trends_data)