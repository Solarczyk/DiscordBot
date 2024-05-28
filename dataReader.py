import requests
import json

url = "https://zsel.edupage.org/timetable/server/regulartt.js"

querystring = {"__func":"regularttGetData"}

payload = "{\"__args\":[null,\"67\"],\"__gsh\":\"00000000\"}"
headers = {
    'accept': "*/*",
    'accept-language': "en-US,en-GB;q=0.9,en;q=0.8,pl-PL;q=0.7,pl;q=0.6",
    'content-type': "application/json; charset=UTF-8",
    'cookie': "PHPSESSID=e94ab95d6dc6be36c33691487898f832",
    'origin': "https://zsel.edupage.org",
    'priority': "u=1, i",
    'referer': "https://zsel.edupage.org/",
    'sec-ch-ua': "'Chromium';v='124', 'Google Chrome';v='124', 'Not-A.Brand';v='99'",
    'sec-ch-ua-mobile': "?0",
    'sec-ch-ua-platform': "'Windows'",
    'sec-fetch-dest': "empty",
    'sec-fetch-mode': "cors",
    'sec-fetch-site': "same-origin",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }

response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
resdata = json.loads(response.text)

def get_data() -> dict:
    return resdata