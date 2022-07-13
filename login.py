import requests
import json
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
import time 



caps = {
    'browserName':'chrome',
    'loggingPrefs': {
        'browser':'ALL',
        'driver':'ALL',
        'performance':'ALL',
    },
    'goog:chromeOptions': {
        'perfLoggingPrefs': {
            'enableNetwork': True,
        },
        'w3c': False, 
    },
}
driver = webdriver.Chrome('C:/Users/danie/Downloads/chromedriver_win32 (5)/chromedriver.exe', desired_capabilities=caps)


driver.get('https://sell.flightclub.com/login')
(print("submitting login"))
time.sleep(4)

email = driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[1]/div[3]/div/div/form/div[1]/div/input').send_keys('#YOUREMAIL')

password = driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[1]/div[3]/div/div/form/div[2]/div/input').send_keys('#YOURPASSWORD')

time.sleep(0.4)

submit = driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[1]/div[3]/div/div/form/div[4]/button').click()

time.sleep(2)

request_log = driver.get_log('performance')

for i in range(len(request_log)):
    message = json.loads(request_log[i]['message'])
    message = message['message']['params']
    request = message.get('request')
    if(request is None):
        continue

    url = request.get('url')
    if(url == "https://sell.flightclub.com/api/me/login"):
        content = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': message['requestId']})
        s1 = json.loads(content['body'])
        token = s1['user']['authenticationToken']
        email = s1['user']['email']
        break

facode = input('2fa code:\n')

addcode = driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[1]/div[3]/div/section/form/div[1]/div/input').send_keys(facode)
time.sleep(2)
submitcode = driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[1]/div[3]/div/section/form/div[2]/button').click()
time.sleep(2)
get_home = driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[1]/div[2]/div/div/a[1]').click

selluuid = driver.get_cookie("_selluuid")
_gat = driver.get_cookie("_gat")
_gid = driver.get_cookie("_gid")
_ga = driver.get_cookie("_ga")
__cf_bm = driver.get_cookie("__cf_bm")

gat = _gat['value']
gid = _gid['value']
ga = _ga['value']
cf = __cf_bm['value']
su = selluuid['value']




headers = {
    'authority': 'sell.flightclub.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'dnt': '1',
    'pragma': 'no-cache',
    'referer': 'https://sell.flightclub.com/home?status=listed',
    'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'x-user-email': email,
    'x-user-token': token,
}

with open('headers.json', 'w', encoding='utf-8') as f:
    json.dump(headers, f, ensure_ascii=False, indent=4)

cookies = {
    '__cf_bm': cf,
    '_ga': ga,
    '_gid': gid,
    '_gat': gat,
    '_selluuid': su,
}
    

  
with open('cookies.json', 'w', encoding='utf-8') as f:
    json.dump(cookies, f, ensure_ascii=False, indent=4)
