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
    get_rate,
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
    {"role": "system", "content": "You are SwapGPT, a bot that allows people to exchange cryptocurrencies. If the user wants to exchange one cryptocurrency for another, he can do it through you."},
    {"role": "system", "content": "You can use create_order function only if you have all the parameters needed to create an order. If you don't have all the parameters, you can use get_price function to get informations about exchange couple requested by user. When you provide the informations to the user, ask him if he wants to create the order. If he wants to create the order, ask for address and amount (if not provided) and then you can use create_order function."},
    {"role": "system", "content": "The revelant minimum and maximum amount is for 'from' currency, not 'to' currency."},
    {"role": "system", "content": "When you create the order. respond only with a feedback on success or fail of order creation."},
    {"role": "system", "content": f"Warning: when a user asks you for information about a crypto (Ex. USDC), consider that for each crypto there may be several different networks. Always ask which network you want to operate for. Possible networks are: {currencies_str}."},
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
        "get_rate": get_rate,
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
        print(function_to_call)
        function_args = json.loads(response_message["function_call"]["arguments"])
        print(function_args)
        function_response = function_to_call(**function_args)
        
        if function_to_call == get_price:
            price_data_json = json.loads(function_response)

            if 'data' in price_data_json and price_data_json['data'] is not None:
                # calcola il tasso di cambio
                from_amount = float(price_data_json['data']['from']['amount'])
                to_amount = float(price_data_json['data']['to']['amount'])
                rate = to_amount / from_amount  # quanto si riceve della valuta 'to' per 1 unità della valuta 'from'

                # aggiungi il rate alla risposta JSON
                price_data_json['data']['exchange_rate'] = rate

                # rimuovi il campo rate dalle singole criptovalute
                del price_data_json['data']['from']['rate']
                del price_data_json['data']['to']['rate']

                if 'error' in price_data_json['data'] and price_data_json['data']['error'] != 0:
                    min_amount = price_data_json['data']['from']['min']
                    from_currency = price_data_json['data']['from']['currency']
                    to_currency = price_data_json['data']['to']['currency']
                    new_price_data = get_price(from_currency, to_currency, min_amount)
                    new_price_data_json = json.loads(new_price_data)

                    # calcola nuovamente il tasso di cambio per la nuova risposta
                    from_amount = float(new_price_data_json['data']['from']['amount'])
                    to_amount = float(new_price_data_json['data']['to']['amount'])
                    rate = str(new_price_data_json['data']['from']['rate'])

                    # crea il messaggio da inserire all'inizio della risposta
                    message = "The minimum amount for this swap is " + str(min_amount) + ". Here is the information for this amount:"
                    exchange_message = "The exchange rate is" + str(rate)

                    # crea una nuova risposta che include il messaggio e la risposta JSON
                    new_response = {
                        'message': message + " " + exchange_message,
                        'response': new_price_data_json
                    }

                    function_response = json.dumps(new_response)
                else:
                    function_response = json.dumps(price_data_json)
            else:
                function_response = "No data found for this exchange couple. Please try again"

       
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
            code = order_data_json.get('code')
            if code == 0:
                function_response = "Order Expiration: " + str(order_data_json['data']['expiration']) + " Finish: " + str(order_data_json['data']['finish']) 
            else:
                function_response = "Order details failed. Reason: " + order_data_json.get('msg', 'Unknown reason')

                
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
    app.run(port=5002, debug=True)

