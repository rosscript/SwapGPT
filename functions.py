import requests
from ffapi.ffapi import ffapi
import os
import json 
import csv, tempfile

api = ffapi(os.getenv("FF_API_KEY"),os.getenv("FF_SECRET_KEY"))

def get_currencies():
    response = api.ccies()
    return response  # assuming this returns a Python object

def filter_currencies(currencies):
    filtered_data = [{"code": x["code"], "coin": x["coin"], "network": x["network"]} for x in currencies]
    return filtered_data  # return a Python object, not a JSON string

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

def delete_order(order_id):
    tempfile_obj = tempfile.NamedTemporaryFile(mode='w', delete=False, newline='')
    writer = csv.writer(tempfile_obj)
    with open('orders.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] != order_id:
                writer.writerow(row)
    tempfile_obj.close()
    os.remove('orders.csv')
    os.rename(tempfile_obj.name, 'orders.csv')

def get_currency_price(code):
    from_ccy_check = check_code(code["fromCcy"])
    amount = code["amount"]
    if from_ccy_check is not True:
        return json.dumps({"error": "Invalid currency codes.", "message": " ".join(from_ccy_check)})
    price_data = {'fromCcy': code["fromCcy"], 'toCcy': 'USDT', 'amount': 1}
    price = get_exchange_price(price_data)
    price_dict = json.loads(price)
    usd_rate = float(price_dict['from']['usd'])
    return str(usd_rate * amount)

                       
def get_exchange_price(price_data):
    errors = []
    from_ccy_check = check_code(price_data["fromCcy"])
    if from_ccy_check is not True:
        errors.append(from_ccy_check)
    to_ccy_check = check_code(price_data["toCcy"])
    if to_ccy_check is not True:
        errors.append(to_ccy_check)
    if errors:
        return json.dumps({"error": "Invalid currency codes.", "message": " ".join(errors)})

    price_data["type"] = "fixed"
    price_data["direction"] = "from"
    response = api.price(price_data)
    return json.dumps(response)

def check_code(code):
    currencies = get_currencies()
    filtered_data = filter_currencies(currencies)
    codes = [item['code'] for item in filtered_data]
    if code not in codes:
        similar_codes = [c for c in codes if c.startswith(code)]
        if similar_codes:
            return f"For {code} you need to choose one specific network: {', '.join(similar_codes)}"
        else:
            return f"{code} is not available or not exist. Ask user to choose another currency."
    else:
        return True

def set_emergency(emergency_data):
    response = api.emergency(emergency_data)
    return json.dumps(response)

def set_email(email_data):
    response = api.setEmail(email_data)
    return json.dumps(response)

def generate_qr(qr_data):
    response = api.qr(qr_data)
    return json.dumps(response)
