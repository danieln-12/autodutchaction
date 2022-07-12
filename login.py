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
driver = webdriver.Chrome('chrome driver directory', desired_capabilities=caps)


driver.get('https://sell.flightclub.com/login')
time.sleep(4)

email = driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[1]/div[3]/div/div/form/div[1]/div/input').send_keys('youremail')

password = driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[1]/div[3]/div/div/form/div[2]/div/input').send_keys('yourpassword')

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
        print(s1['user']['authenticationToken'])
        break

_selluuid = driver.get_cookie("_selluuid")
_gat = driver.get_cookie("_gat")
_gid = driver.get_cookie("_gid")
_ga = driver.get_cookie("_ga")
__cf_bm = driver.get_cookie("__cf_bm")

cookies = {
    '__cf_bm': __cf_bm['value'],
    '_ga': _ga['value'],
    '_gid': _gid['value'],
    '_gat': _gat['value'],
    '_selluuid': _selluuid['value'],
}
