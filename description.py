initial_prompt = [
    {"role": "system", "content": "You are SwapGPT, a bot that allows people to exchange cryptocurrencies. If the user wants to exchange one cryptocurrency for another, he can do it through you."},
    {"role": "system", "content": "You can use create_order function only if you have all the parameters needed to create an order. If you don't have all the parameters, you can use get_price function to get informations about exchange couple requested by user. When you provide the informations to the user, ask him if he wants to create the order. If he wants to create the order, ask for address and amount (if not provided) and then you can use create_order function."},
    {"role": "system", "content": "The revelant minimum and maximum amount is for 'from' currency, not 'to' currency."},
    {"role": "system", "content": "When you create the order. respond only with a feedback on success or fail of order creation."},
]

functions_description = [
    {
        "name": "create_order",
        "description": "Creates an exchange order with the provided parameters. Ask to user all the parameters, dont't use default/example values.",
        "parameters": {
            "type": "object",
            "properties": {
                "fromCcy": {
                    "type": "string",
                    "description": "The currency to exchange from."
                },
                "toCcy": {
                    "type": "string",
                    "description": "The currency to exchange to."
                },
                "amount": {
                    "type": "number",
                    "description": "The amount of currency to exchange."
                },
                "toAddress": {
                    "type": "string",
                    "description": "The address to which the exchanged currency should be sent."
                }
            },
            "required": ["fromCcy", "toCcy", "amount", "toAddress"]
        }
    },
    {
        "name": "get_order",
        "description": "Returns the details of an order. First you need to ask user for order ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "The id of the order to retrieve.",
                }
            },
            "required": ["order_id"],
        },
    },
    {
        "name": "delete_order",
        "description": "Delete the order. First you need to ask user for order ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "The id of the order to delete.",
                }
            },
            "required": ["order_id"],
        },
    },
    {
        "name": "get_exchange_price",
        "description": "Returns the conversion rate between two currencies.",
        "parameters": {
            "type": "object",
            "properties": {
                "fromCcy": {
                    "type": "string",
                    "description": "The currency to convert from. Ex: BTC, ETH, etc.",
                },
                "toCcy": {
                    "type": "string",
                    "description": "The currency to convert to. Ex: BTC, ETH, etc.",
                },
                "amount": {
                    "type": "number",
                    "description": "The amount of the 'from' currency to convert.",
                }
            },
            "required": ["fromCcy", "toCcy", "amount"],
        },
    },
    {
        "name": "get_currency_price",
        "description": "Returns the rate for given currency againist USDT.",
        "parameters": {
            "type": "object",
            "properties": {
                "fromCcy": {
                    "type": "string",
                    "description": "The currency to get price in USDT. Ex: BTC, ETH, etc.",
                },
                "amount": {
                    "type": "number",
                    "description": "The amount of the 'from' currency to get price.",
                }
            },
            "required": ["fromCcy", "amount"],
        },
    }
]

