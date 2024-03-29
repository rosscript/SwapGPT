from dotenv import load_dotenv
import os, tempfile
import json
import csv
from flask import Flask, request, jsonify, render_template, session
from flask_session import Session
from jinja2 import Environment, select_autoescape
import openai
from description import functions_description, initial_prompt
from functions import (
    get_currencies,
    create_order,
    get_order,
    get_token,
    get_exchange_price,
    generate_qr,
    save_order,
    filter_currencies,
    delete_order,
    get_currency_price,
)


load_dotenv()
openai.api_key = os.getenv("OPENAI_SECRET_KEY")

app = Flask(__name__,
            static_url_path='', 
            static_folder='web/static',
            template_folder='web/templates')

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_FILE_DIR'] = tempfile.mkdtemp()
Session(app)

def clear_messages(filtered_currencies):
    session['messages'] = []
    session['messages'].extend(initial_prompt)
    session['messages'].append({"role": "system", "content": f"Warning: when a user asks you for information about a crypto (Ex. USDC), consider that for each crypto there may be several different networks. Always ask which network you want to operate for. Possible networks are: {filtered_currencies}."})

#Cancella tutti i messaggi tranne lo stato iniziale
def limit_messages():
    if len(session['messages']) > 5:
        session['messages'] = session['messages'][:5]

#Cancella i messaggi 6 e 7 (la prima domanda e risposta)
def pop_sixth_message():
    session['messages'].pop(6)
    session['messages'].pop(6)

def run_conversation(user_message):
    session['messages'].append({"role": "user", "content": user_message})
    order_data = None
     
    available_functions = {
        "create_order": create_order,
        "get_order": get_order,
        "get_exchange_price": get_exchange_price,
        "delete_order": delete_order,
        "get_currency_price": get_currency_price,
    }

    while True:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=session['messages'],
            functions=functions_description,
            function_call="auto",
        )
        response_message = response["choices"][0]["message"]
        session['messages'].append(response_message)
        
        if not response_message.get("function_call"):
            break

        function_name = response_message["function_call"]["name"]
        function_to_call = available_functions.get(function_name)

        if function_to_call is not None:
            function_args = json.loads(response_message["function_call"]["arguments"])
            print(function_to_call, function_args)
        else:
            print(f"Function '{function_name}' not found in available functions.")

        
        try:
            function_response = function_to_call(function_args)
        except Exception as e:
            return str(e), order_data
        
        if function_to_call == get_exchange_price:
            limit_messages()
            price_data_json = json.loads(function_response)
            del price_data_json['to']
            if 'errors' in price_data_json and 'LIMIT_MAX' in price_data_json['errors']:
                del price_data_json['errors']
            if 'errors' in price_data_json and 'LIMIT_MIN' in price_data_json['errors']:
                del price_data_json['errors']
                
        if function_to_call == create_order:
            limit_messages()
            order_data = function_response
            order_data_json = json.loads(order_data)
            if order_data_json['status'] == "NEW":
                function_response = "Order created successfully: " + order_data_json['id'] + ". Please save this order ID."
                save_order(order_data_json['id'], order_data_json['token'])
                qr_data = {"id": order_data_json['id'], "token": order_data_json['token']}
                qr_response_str = generate_qr(qr_data)
                order_data = json.loads(order_data)
                qr_response = json.loads(qr_response_str)
                for item in qr_response:
                    if item['title'] == 'Address':
                        order_data['qr_data'] = item['src']
                        break
                order_data = json.dumps(order_data)
            else:
                function_response = "Order creation failed. Reason: " + order_data_json

        if function_to_call == get_order:
            order_data = function_response
            order_data_json = json.loads(order_data)
            if order_data_json['id']:
                function_response = "Order retrieved successfully: " + order_data_json['id'] + ". Status: " + order_data_json['status'] + "."     
                qr_data = {"id": order_data_json['id'], "token": order_data_json['token']}
                qr_response_str = generate_qr(qr_data)
                order_data = json.loads(order_data)
                qr_response = json.loads(qr_response_str)
                for item in qr_response:
                    if item['title'] == 'Address':
                        order_data['qr_data'] = item['src']
                        break
                order_data = json.dumps(order_data)
            else:
                function_response = "Failed. Reason: " + order_data_json
 
        session['messages'].append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )

    return response["choices"][0]["message"]["content"], order_data

@app.route('/process_message', methods=['POST'])
def process_message():
    if 'messages' in session and len(session['messages']) > 12:
        pop_sixth_message()
    data = request.get_json()
    user_message = data.get("message", "")
    print("Message array length: " + str(len(session.get('messages', []))))
    response, order_data = run_conversation(user_message)

    return jsonify({"response": response, "order_data": order_data})

@app.route('/order/<order_id>')
def get_order_page(order_id):
    try:
        currencies = get_currencies()
        filtered_currencies = filter_currencies(currencies)
        clear_messages(filtered_currencies)
        currencies = json.loads(currencies)
        order_data = get_order({'order_id': order_id})
        order_data_json = json.loads(order_data)
        return render_template('order.html', order=order_data_json, order_id=order_id, currencies=currencies)
    except Exception as e:
        app.logger.error(f"Error when loading currencies: {e}")
        return render_template('maintenance.html')

    
@app.route('/')
def index():
    if 'messages' not in session:
        session['messages'] = []
    try:
        currencies = get_currencies()
        filtered_currencies = filter_currencies(currencies)
        clear_messages(filtered_currencies)
        return render_template('index.html', currencies=currencies)
    except Exception as e:
        app.logger.error(f"Error when loading currencies: {e}")
        return render_template('maintenance.html')

    
if __name__ == "__main__":
    app.run(port=5000, debug=True)

