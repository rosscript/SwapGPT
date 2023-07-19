import requests
from FixedFloatApi import FixedFloatApi
import os
import json 
import csv

api = FixedFloatApi(os.getenv("FF_API_KEY"),os.getenv("FF_SECRET_KEY"))

def get_currencies():
    response = api.ccies()
    return json.dumps(response)

def create_order(order_data):
    order_data["type"] = "fixed"
    order_data["direction"] = "from"
    response = api.create(order_data)
    return json.dumps(response)

def get_order(data):
    order_id = data['order_id']
    token = get_token(order_id)
    if token is None:
        return json.dumps({"error": "Order not found."})
    order_info = {"id": order_id, "token": token}
    response = api.order(order_info)
    return json.dumps(response)


def get_token(order_id):
    with open('orders.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == order_id:
                return row[1]
    return None

def save_order(order_id, token):
    with open('orders.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([order_id, token]) 
                    
def get_exchange_price(price_data):
    price_data["type"] = "fixed"
    price_data["direction"] = "from"
    print(price_data)
    response = api.price(price_data)
    return json.dumps(response)

def set_emergency(emergency_data):
    response = api.emergency(emergency_data)
    return json.dumps(response)

def set_email(email_data):
    response = api.setEmail(email_data)
    return json.dumps(response)

def generate_qr(qr_data):
    response = api.qr(qr_data)
    return json.dumps(response)

def filter_currencies(currencies):
    # Convert the string to a list of dictionaries
    data = json.loads(currencies)

    # Create a new list with dictionaries that only contain the keys you're interested in
    filtered_data = [{"code": x["code"], "coin": x["coin"], "network": x["network"]} for x in data]

    # Convert the list back to a JSON string
    filtered_currencies = json.dumps(filtered_data)

    return filtered_currencies