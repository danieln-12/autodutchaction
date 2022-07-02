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
   
}

email = input('Email:\n')
user_token = input('User Token:\n')
headers = {
    'authority': 'sell.flightclub.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'pragma': 'no-cache',
    'referer': 'https://sell.flightclub.com/home?status=listed',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    'x-user-email': email,
    'x-user-token': user_token,
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
    
    my_ids={}
    for i in range(len(listing_ids)):
        response = requests.get(f'https://sell.flightclub.com/api/me/stock/{listing_ids[i]}/pricing', cookies=cookies, headers=headers) 
        response_price = response.json()
        
        
    
        price = response_price['priceCents']
        id = response_price['stockItemId']
        item = response_price['product']['name']
        lowest_ask = response_price['currentLowestPrice']

        
        print(style.MAGENTA + f'[{datetime.now()}] => Current Price: {price/100:.2f} | Lowest Price: {lowest_ask/100:.2f} | ID: {id} | Item: {item}')
        
        if price > lowest_ask:
            my_ids[price]=[lowest_ask-100] 
            print(style.WHITE + f'[{datetime.now()}] => over lowest ask[{price/100:.2f}][{id}]')
            prices = price
            ids = id
            #result = zip(ids, prices)
            #print(range(result))
            
    
    print(style.WHITE + f'{my_ids}') #undercut prices
       
main()
