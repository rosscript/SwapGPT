# Esempi di richieste HTTP per testare l'API con Postman

## GET /get_currencies

- URL: `http://localhost:5000/get_currencies`
- Metodo: GET
- Nessun body o parametri necessari.

## POST /create_order

- URL: `http://localhost:5000/create_order`
- Metodo: POST
- Body (formato JSON):

```json
{
  "from_currency": "BTC",
  "to_currency": "ETH",
  "amount": 0.01,
  "destination_address": "0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B",
  "type": "fixed"
}
```

## GET /get_order

- URL: `http://localhost:5000/get_order?order_id=abc123&token=def456`
- Metodo: GET
- Parametri della query:
  - order_id: abc123
  - token: def456

## GET /get_price

- URL: `http://localhost:5000/get_price?from_currency=BTC&to_currency=ETH&amount=0.01&type=fixed`
- Metodo: GET
- Parametri della query:
  - from_currency: BTC
  - to_currency: ETH
  - amount: 0.01
  - type: fixed

## POST /set_emergency

- URL: `http://localhost:5000/set_emergency`
- Metodo: POST
- Body (formato JSON):

```json
{
  "order_id": "abc123",
  "token": "def456",
  "exchange": "binance"
}
