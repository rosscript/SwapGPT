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
