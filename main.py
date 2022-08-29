
import requests
from datetime import datetime
import json
from datetime import datetime
import time
import os
import login

#login call
login.my_func()


# System call
os.system("")

# Class of different styles
class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'


f = open('headers.json')
headers = json.load(f)


i = open('cookies.json')
cookies = json.load(i)


def main():
    print(style.YELLOW + f'[{datetime.now()}] => getting manifest[request/count]')
    response = requests.get('https://sell.flightclub.com/api/me/listings/summary', cookies=cookies, headers=headers)
    mnfl = response.json()
    cnt = mnfl[1]
    ppage = cnt['count']
    print(style.YELLOW + f'[{datetime.now()}] => getting listing ids[request/listings]')
    params = {
        'direction': 'desc',
        'perPage': ppage,
        'sort': 'created_at',
        'status': [
            'on_sale',
            'hidden',
            'missing',
            'needs_validation',
            'on_hold',
            'pending_writeoff',
            'reserved',
            ],
    }
    response = requests.get('https://sell.flightclub.com/api/me/listings', params=params, cookies=cookies, headers=headers)
    response_data_ids = response.json()
    if response.status_code == 200:
        print(style.GREEN + f'[{datetime.now()}] => got listing ids[status:{response.status_code}]')
    else:
        print(style.RED + f'[{datetime.now()}] => error [{response.status_code}][{response}][auth error]')
        time.sleep(3) #retry delay
        main()
    
    listing_ids = [result['id'] for result in response_data_ids['results']]
    
    id_ucprice= []
    for i in range(len(listing_ids)):
        response = requests.get(f'https://sell.flightclub.com/api/me/stock/{listing_ids[i]}/pricing', cookies=cookies, headers=headers) 
        time.sleep(0.2) #listing delay
        response_price = response.json()

        price = response_price['priceCents']
        id = response_price['stockItemId']
        item = response_price['product']['name']
        response = requests.get(f'https://sell.flightclub.com/api/me/stock/{listing_ids[i]}', cookies=cookies, headers=headers) 
        response_status = response.json()
        lowest_ask = response_status['lowestConsignedPriceCents']
        payout = ((0.905 * price) - 500 ) *0.971
        l1ask = response_status['marketPriceCents']
        
        if response_status["status"] == "reserved":
            print(style.BLUE + f'[{datetime.now()}] => Pending Sold | Payout => {payout/100:.2f} | ID => {id} | Item => {item}')
        elif response_status["status"] == "hidden":
            print(style.WHITE + f'[{datetime.now()}] => Unknown Status: {response_status["status"]} | Payout => {payout/100:.2f} | ID => {id} | Item => {item}')
        elif response_status["status"] == "missing":
            print(style.WHITE + f'[{datetime.now()}] => Unknown Status: {response_status["status"]} | Payout => {payout/100:.2f} | ID => {id} | Item => {item}')
        elif response_status["status"] == "pending_writeoff":
            print(style.WHITE + f'[{datetime.now()}] => Unknown Status: {response_status["status"]} | Payout => {payout/100:.2f} | ID => {id} | Item => {item}')
        elif response_status["status"] == "needs_validation":
            print(style.WHITE + f'[{datetime.now()}] => Unknown Status: {response_status["status"]} | Payout => {payout/100:.2f} | ID => {id} | Item => {item}')
        elif len(response_status['conditions']) == True:
            cond1 = response_status['conditions'][0]
            print(style.MAGENTA + f'[{datetime.now()}] => Listed | Conditions => "{cond1}" | Current Price => {price/100:.2f} | Lowest Price => {l1ask/100:.2f} | ID => {id} | Item => {item}')
        elif lowest_ask == None:
            print(style.MAGENTA + f'[{datetime.now()}] => Listed | Current Price => {price/100:.2f} | Lowest Price => n/a | ID => {id} | Item => {item}')
        else:
            print(style.MAGENTA + f'[{datetime.now()}] => Listed | Current Price => {price/100:.2f} | Lowest Price => {lowest_ask/100:.2f} | ID => {id} | Item => {item}')
            if price > lowest_ask:
                id_ucprice.append([id,lowest_ask-100])
                print(style.RED + f'[{datetime.now()}] => Over Lowest Ask [{price/100:.2f}][{id}]')

    for ids in id_ucprice:
        post_data = {
        'price': ids[1],
        'overpriced_email_price_change': False,
        'apply_to_all': False,
        }
        response = requests.post(f'https://sell.flightclub.com/api/me/stock/{ids[0]}/pricing', cookies=cookies, headers=headers, json=post_data)
        time.sleep(0.8) #update delay
        update_data = json.loads(response.text)
        if update_data["priceCents"] == ids[1]:
            print(style.GREEN + f'[{datetime.now()}] => ' f'Updated Ask => ${update_data["priceCents"]/100:.2f} '
              f'| ID => {update_data["id"]}' 
              f' | Item => {update_data["name"]}')
        else:
            print(style.RED + f'[{datetime.now()}] => unknown status[{response.text}]')

main()
