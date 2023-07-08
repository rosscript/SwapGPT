import requests
import json
import csv

BASE_URL = 'http://localhost:5001/'

def get_currencies():
    url = BASE_URL + 'get_currencies'
    response = requests.get(url)
    return response.json()  # Directly return the JSON response as a Python dictionary


def get_rate(from_currency_amount, rate):
    print(from_currency_amount, rate)
    return str(from_currency_amount * rate)

    
def create_order(from_currency, to_currency, amount, destination_address, type='fixed'):
    url = BASE_URL + 'create_order'
    data = {
        'from_currency': from_currency,
        'to_currency': to_currency,
        'amount': amount,
        'destination_address': destination_address,
        'type': type
    }
    response = requests.post(url, json=data)
    print(response.json())
    return json.dumps(response.json())

def get_order(order_id):
    token = get_token(order_id)
    if token is None:
        return json.dumps({"error": "No token found for the provided order_id."})
    url = BASE_URL + 'get_order'
    params = {
        'order_id': order_id,
        'token': token
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 404:
        return json.dumps({"error": f"Order id {order_id} was not found."})

    return json.dumps(response.json())


def get_token(order_id):
    with open('orders.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == order_id:
                return row[1]
    return None

def get_price(from_currency, to_currency, amount, type='fixed'):
    url = BASE_URL + 'get_price'
    params = {
        'from_currency': from_currency,
        'to_currency': to_currency,
        'amount': amount,
        'order_type': type
    }
    response = requests.get(url, params=params)
    return json.dumps(response.json())

def set_emergency(order_id, token, exchange):
    url = BASE_URL + 'set_emergency'
    data = {
        'order_id': order_id,
        'token': token,
        'exchange': exchange
    }
    response = requests.post(url, json=data)
    return json.dumps(response.json())
