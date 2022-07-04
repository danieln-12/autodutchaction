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
#fix auto user cookies
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
    'x-user-email': email,
    'x-user-token': authtoken,
}

params = {
    'direction': 'desc',
    'perPage': '80', #can edit depending on how many you want to sort
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
    print(style.YELLOW + f'[{datetime.now()}] => getting listing ids[]')
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
        lowest_ask = response_price['currentLowestPrice']
        response = requests.get(f'https://sell.flightclub.com/api/me/stock/{listing_ids[i]}', cookies=cookies, headers=headers) 
        response_status = response.json()
        pending = response_status["status"]
        payout = ((0.905 * price) - 500 ) *0.971
        
        if pending == "reserved":
                print(style.BLUE + f'[{datetime.now()}] => Pending Sold | Payout => {payout/100:.2f} | ID => {id} | Item => {item}')
        else:
            print(style.MAGENTA + f'[{datetime.now()}] => Listed | Current Price => {price/100:.2f} | Lowest Price => {lowest_ask/100:.2f} | ID => {id} | Item => {item}')
            if price > lowest_ask:
                id_ucprice.append([id,lowest_ask-100])
                print(style.RED + f'[{datetime.now()}] => Over Lowest Ask [{price/100:.2f}][{id}]')
        

     

        response = requests.get(f'https://sell.flightclub.com/api/me/stock/{listing_ids[i]}', cookies=cookies, headers=headers) 
        response_status = response.json()
        

    for ids in id_ucprice:
        post_data = {
        'price': ids[1],
        'overpriced_email_price_change': False,
        'apply_to_all': False,
        }
        response = requests.post(f'https://sell.flightclub.com/api/me/stock/{ids[0]}/pricing', cookies=cookies, headers=headers, json=post_data)
        update_data = json.loads(response.text)
        response_price = update_data['priceCents']
        r_item = update_data['name']
        r_id = update_data['id']
        unelgible = "{'message': 'This item is not currently eligible for a price adjustment. Please try again later.'}"
        if update_data == unelgible:
            print(style.RED + f'[{datetime.now()}] => Failed Updating | ID = > {r_id} | Item => {r_item}')
            
        if response_price == ids[1]:
            print(style.GREEN + f'[{datetime.now()}] => Updated Price: {response_price/100:.2f} | ID = > {r_id} | Item => {r_item}')

main()


#fix iteration and response {'message': 'id is invalid'}
