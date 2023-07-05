import requests
import hmac
import hashlib

class FixedFloat:
    def __init__(self, api_pub, api_secret, api_url = "https://fixedfloat.com/api/v1/") -> None:
        self.api_pub = api_pub
        self.api_secret_bytes = bytearray(api_secret, 'utf-8')
        self.api_url = api_url

    def __sign_request__(self, params):
        return hmac.new(self.api_secret_bytes, bytearray(params, 'utf-8'), hashlib.sha256).hexdigest()

    def __get_request_headers__(self, signed_params):
        header = {
            "X-API-KEY": self.api_pub,
            "X-API-SIGN": signed_params,
            }
        return header

    def __send_request__(self, endpoint, header, data=None, is_post = False):
        if is_post:
            answer = requests.post(self.api_url + endpoint, headers=header, data=data)
        else:
            answer = requests.get(self.api_url + endpoint, headers=header, params=data if data else None)
        return answer.content

    def get_currencies(self):
        endpoint = "getCurrencies"
        params = ""
        signed_params = self.__sign_request__(params=params)
        header = self.__get_request_headers__(signed_params=signed_params)

        return self.__send_request__(endpoint=endpoint, header=header)

    def get_price(self, from_currency: str, from_qty: float, to_currency: str, type: str):
        endpoint = "getPrice"
        params = f"fromCurrency={from_currency}&fromQty={from_qty}&toCurrency={to_currency}&type={type}"
        signed_params = self.__sign_request__(params=params)
        header = self.__get_request_headers__(signed_params=signed_params)
        data = {
            "fromCurrency": from_currency,
            "fromQty": from_qty,
            "toCurrency": to_currency,
            "type": type
        }

        return self.__send_request__(endpoint=endpoint, header=header, data=data, is_post=True)

    def create_order(self, from_currency: str, to_currency: str, from_qty: float, to_address: str, type: str):
        endpoint = "createOrder"
        params = f"fromCurrency={from_currency}&toCurrency={to_currency}&fromQty={from_qty}"\
            f"&toAddress={to_address}&type={type}"

        signed_params = self.__sign_request__(params=params)

        header = self.__get_request_headers__(signed_params=signed_params)

        data = {
            "fromCurrency": from_currency,
            "toCurrency": to_currency,
            "fromQty": from_qty,
            "toAddress": to_address,
            "type": type
        }

        return self.__send_request__(endpoint=endpoint, header=header, data=data, is_post=True)

    def get_order(self, id: str, token: str):
        endpoint = "getOrder"
        params = f"id={id}&token={token}"
        signed_params = self.__sign_request__(params=params)
        header = self.__get_request_headers__(signed_params=signed_params)

        data = {
            "id": id,
            "token": token
        }

        return self.__send_request__(endpoint=endpoint, header=header, data=data)

    def set_emergency(self, id: str, token: str, choice: str, address=None):
        endpoint = "setEmergency"
        params = ""
        if choice == "EXCHANGE":
            params = f"id={id}&token={token}&choice={choice}"
        if (choice == "REFUND") and (address != None):
            params = f"id={id}&token={token}&choice={choice}&address={address}"
        
        signed_params = self.__sign_request__(params=params)

        header = self.__get_request_headers__(signed_params=signed_params)

        data = {
            "id": id,
            "token": token,
            "choice": choice,
        }

        if choice == "REFUND":
            data['address'] = address

        return self.__send_request__(endpoint=endpoint, header=header, data=data, is_post=True) if params else False