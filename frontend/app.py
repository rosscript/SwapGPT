from dotenv import load_dotenv
import os
import json
import csv
from flask import Flask, request, jsonify, render_template
import openai
from functions_description import functions_description
from functions import (
    get_currencies,
    create_order,
    get_order,
    get_token,
    get_price,
    set_emergency
)

app = Flask(__name__)
messages = []
load_dotenv()
openai.api_key = os.getenv("OPENAI_SECRET_KEY")

currencies = get_currencies()
currencies_list = currencies.get('data', [])
currencies_info = [{'currency': currency['currency'], 
                    'name': currency['name'], 
                    'network': currency['network']} 
                    for currency in currencies_list]

# Format the currencies list into a string
currencies_str = ", ".join([f"{c['name']} (currency: {c['currency']}, network: {c['network']})" for c in currencies_info])

messages = [
    {"role": "system", "content": "You are SwapGPT, a bot that allows people to exchange cryptocurrencies. If the user wants to exchange one cryptocurrency for another, he can do it through you. If the user is not precise and confident enough from the start, guide him through the workflow: 1-Visualize the details of a given cryptocurrency pair. 2-Create the actual order. If it doesn't give you all the parameters you need, you need to ask the user before trying to run the create order function."},
    {"role": "system", "content": "When you create the order. respond only with a feedback on success or fail of order creation."},
    {"role": "system", "content": f"Available cryptocurrencies: {currencies_str}."},
]

app = Flask(__name__,
            static_url_path='', 
            static_folder='web/static',
            template_folder='web/templates')

def run_conversation(user_message):
    global messages
    messages.append({"role": "user", "content": user_message})
    order_data = None
    
    available_functions = {
        "create_order": create_order,
        "get_order": get_order,
        "get_token": get_token,
        "get_price": get_price,
        "set_emergency": set_emergency
    }

    while True:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
            functions=functions_description,
            function_call="auto",
        )
        response_message = response["choices"][0]["message"]
        messages.append(response_message)

        if not response_message.get("function_call"):
            break

        function_name = response_message["function_call"]["name"]
        function_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        function_response = function_to_call(**function_args)
        
        if function_to_call == create_order:
            order_data = function_response
            order_data_json = json.loads(order_data)
            if order_data_json['code'] == 0:
                function_response = "Order created successfully! (Data passed in backend to frontend)"
                # Salviamo l'Order ID e il token in un file CSV
                with open('orders.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([order_data_json['data']['id'], order_data_json['data']['token']])    
            else:
                function_response = "Order creation failed. Reason: " + order_data_json['msg']

        if function_to_call == get_order:
            order_data = function_response
            order_data_json = json.loads(order_data)
            if order_data_json['code'] == 0:
                function_response = "Expiration: " + str(order_data_json['data']['expiration']) + " Finish: " + str(order_data_json['data']['finish']) 
            else:
                function_response = "Order details failed. Reason: " + order_data_json['msg']
                
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )

    return response["choices"][0]["message"]["content"], order_data

@app.route('/process_message', methods=['POST'])
def process_message():
    data = request.get_json()
    user_message = data.get("message", "")

    response, order_data = run_conversation(user_message)

    return jsonify({"response": response, "order_data": order_data})

@app.route('/')
def index():
    currencies = get_currencies()
    currencies_list = currencies.get('data', [])
    currencies_info = [{'currency': currency['currency'], 
                        'name': currency['name'], 
                        'network': currency['network']} 
                       for currency in currencies_list]
    
    # Format the currencies list into a string
    currencies_str = ", ".join([f"{c['name']} (currency: {c['currency']}, network: {c['network']})" for c in currencies_info])

    return render_template('index.html', currencies_info=currencies_info)

if __name__ == "__main__":
    app.run(port=5000, debug=True)

