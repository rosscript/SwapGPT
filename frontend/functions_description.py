functions_description = [
    {
        "name": "create_order",
        "description": "Creates an order for a currency exchange.",
        "parameters": {
            "type": "object",
            "properties": {
                "from_currency": {
                    "type": "string",
                    "description": "The currency to convert from. Ex: BTC, ETH, etc.",
                },
                "to_currency": {
                    "type": "string",
                    "description": "The currency to convert to. Ex: BTC, ETH, etc.",
                },
                "amount": {
                    "type": "number",
                    "description": "The amount of the 'from' currency to convert.",
                },
                "destination_address": {
                    "type": "string",
                    "description": "The address to send the converted currency to.",
                },
                "type": {
                    "type": "string",
                    "description": "The type of the order, either 'fixed' or 'float'.",
                }
            },
            "required": ["from_currency", "to_currency", "amount", "destination_address"],
        },
    },
    {
        "name": "get_rate",
        "description": "Calculates the amount of target cryptocurrency (crypto B) obtained from a certain amount of source cryptocurrency (crypto A) based on the exchange rate.",
        "parameters": {
            "type": "object",
            "properties": {
                "from_currency_amount": {
                    "type": "number",
                    "description": "The amount of the source cryptocurrency that you want to exchange."
                },
                "rate": {
                    "type": "number",
                    "description": "The exchange rate between the source and target cryptocurrency. It indicates how many units of the target cryptocurrency you get for one unit of the source cryptocurrency."
                }
            },
            "required": ["from_currency_amount", "rate"]
        },
        "returns": {
            "type": "number",
            "description": "The amount of target cryptocurrency that will be obtained based on the input amount of source cryptocurrency and the exchange rate."
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
        "name": "get_price",
        "description": "Returns the conversion rate between two currencies.",
        "parameters": {
            "type": "object",
            "properties": {
                "from_currency": {
                    "type": "string",
                    "description": "The currency to convert from. Ex: BTC, ETH, etc.",
                },
                "to_currency": {
                    "type": "string",
                    "description": "The currency to convert to. Ex: BTC, ETH, etc.",
                },
                "amount": {
                    "type": "number",
                    "description": "The amount of the 'from' currency to convert.",
                },
                "type": {
                    "type": "string",
                    "description": "The type of the conversion, either 'fixed' or 'float'.",
                }
            },
            "required": ["from_currency", "to_currency", "amount"],
        },
    },
    {
        "name": "set_emergency",
        "description": "Sets an emergency address for a given order.",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "The id of the order to set the emergency address for.",
                },
                "token": {
                    "type": "string",
                    "description": "The token associated with the order.",
                },
                "exchange": {
                    "type": "string",
                    "description": "The address to be used in case of emergency.",
                }
            },
            "required": ["order_id", "token", "exchange"],
        },
    },
]
