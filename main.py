import email
from itertools import product
from unittest import result
import requests
from datetime import datetime
import json
from datetime import datetime
import time
import os

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



cookies = {
#copy cookies from /listed response(don't expire afaik),
}

headers = {
    'authority': 'sell.flightclub.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
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
    'x-user-email': #youremail,
    'x-user-token': #yourtoken,
}

params = {
    'direction': 'desc',
    'perPage': '80',
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

def main():
    print(style.YELLOW + f'[{datetime.now()}] => getting listing ids[request/listings]')
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
        response_price = response.json()

        price = response_price['priceCents']
        id = response_price['stockItemId']
        item = response_price['product']['name']
        response = requests.get(f'https://sell.flightclub.com/api/me/stock/{listing_ids[i]}', cookies=cookies, headers=headers) 
        response_status = response.json()
        lowest_ask = response_status['lowestConsignedPriceCents']
        payout = ((0.905 * price) - 500 ) *0.971
        
        if response_status["status"] == "reserved":
                print(style.BLUE + f'[{datetime.now()}] => Pending Sold | Payout => {payout/100:.2f} | ID => {id} | Item => {item}')
        elif response_status["status"] == "hidden":
            print(style.WHITE + f'[{datetime.now()}] => Unknown Status: Hidden | Payout => {payout/100:.2f} | ID => {id} | Item => {item}')
        elif response_status["status"] == "missing":
            print(style.WHITE + f'[{datetime.now()}] => Unknown Status: Missing | Payout => {payout/100:.2f} | ID => {id} | Item => {item}')
        elif response_status["status"] == "pending_writeoff":
            print(style.WHITE + f'[{datetime.now()}] => Unknown Status: Pending Writeoff | Payout => {payout/100:.2f} | ID => {id} | Item => {item}')
        elif response_status["status"] == "needs_validation":
            print(style.WHITE + f'[{datetime.now()}] => Unknown Status: Needs Validation | Payout => {payout/100:.2f} | ID => {id} | Item => {item}')
        elif lowest_ask == None:
                print(style.MAGENTA + f'[{datetime.now()}] => Listed | Current Price => {price/100:.2f} | Lowest Price => N/A | ID => {id} | Item => {item}')
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
        update_data = json.loads(response.text)
        if update_data["priceCents"] == ids[1]:
            print(style.GREEN + f'[{datetime.now()}] => ' f'Updated Ask => ${update_data["priceCents"]/100:.2f} '
              f'| ID = > {update_data["id"]}' 
              f' | Item => {update_data["name"]}')
        else:
            print(style.RED + f'[{datetime.now()}] => unknown status[{response.text}]')


main()
