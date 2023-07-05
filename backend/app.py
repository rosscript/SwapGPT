from flask import Flask, request, jsonify
from fixedfloat.fixedfloat import FixedFloat
from dotenv import load_dotenv
import os
import json

app = Flask(__name__)

load_dotenv()
api = FixedFloat(os.getenv("API_KEY"), os.getenv("SECRET_KEY"))

@app.route('/get_currencies', methods=['GET'])
def get_currencies():
    currencies_bytes = api.get_currencies()
    currencies_str = currencies_bytes.decode('utf-8')
    currencies_obj = json.loads(currencies_str)
    return jsonify(currencies_obj)

@app.route('/create_order', methods=['POST'])
def create_order():
    data = request.get_json()
    from_currency = data.get("from_currency", "")
    to_currency = data.get("to_currency", "")
    amount = float(data.get("amount", 0))
    destination_address = data.get("destination_address", "")
    order_type = data.get("type", "fixed")
    order_bytes = api.create_order(from_currency, to_currency, amount, destination_address, order_type)
    order_str = order_bytes.decode('utf-8')
    order_obj = json.loads(order_str)
    return jsonify(order_obj)

@app.route('/get_order', methods=['GET'])
def get_order():
    order_id = request.args.get('order_id', "")
    token = request.args.get('token', "")
    order_bytes = api.get_order(order_id, token)
    order_str = order_bytes.decode('utf-8')
    order_obj = json.loads(order_str)
    return jsonify(order_obj)

@app.route('/get_price', methods=['GET'])
def get_price():
    from_currency = request.args.get('from_currency', "")
    to_currency = request.args.get('to_currency', "")
    amount = float(request.args.get('amount', 0))
    type = request.args.get('type', "fixed")
    price_bytes = api.get_price(from_currency, amount, to_currency, type)
    price_str = price_bytes.decode('utf-8')
    price_obj = json.loads(price_str)
    return jsonify(price_obj)

@app.route('/set_emergency', methods=['POST'])
def set_emergency():
    data = request.get_json()
    order_id = data.get("order_id", "")
    token = data.get("token", "")
    exchange = data.get("exchange", "")
    response_bytes = api.set_emergency(order_id, token, exchange)
    response_str = response_bytes.decode('utf-8')
    response_obj = json.loads(response_str)
    return jsonify(response_obj)

if __name__ == "__main__":
    app.run(port=5001, debug=True)

