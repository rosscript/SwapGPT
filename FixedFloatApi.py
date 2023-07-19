import requests
import json
import hmac
import hashlib

class FixedFloatApi:
    RESP_OK = 0
    TYPE_FIXED = 'fixed'
    TYPE_FLOAT = 'float'

    def __init__(self, key, secret):
        self.key = key
        self.secret = secret

    def sign(self, data):
        if isinstance(data, dict):
            parts = ['{}={}'.format(k, v) for k, v in data.items()]
            str_to_sign = '&'.join(parts)
        else:
            str_to_sign = data
        return hmac.new(bytes(self.secret , 'latin-1'), msg = bytes(str_to_sign , 'latin-1'), digestmod = hashlib.sha256).hexdigest()

    def req(self, method, data):
        url = 'https://ff.io/api/v2/' + method
        req = json.dumps(data)
        headers = {
            'Content-Type': 'application/json',
            'X-API-KEY': self.key,
            'X-API-SIGN': self.sign(req)
        }
        response = requests.post(url, data=req, headers=headers)
        result = response.json()
        if result['code'] == self.RESP_OK:
            return result['data']
        else:
            raise Exception(result['msg'], result['code'])

    def ccies(self):
        return self.req('ccies', {})

    def price(self, data):
        return self.req('price', data)

    def create(self, data):
        return self.req('create', data)

    def order(self, data):
        return self.req('order', data)

    def emergency(self, data):
        return self.req('emergency', data)

    def setEmail(self, data):
        return self.req('setEmail', data)

    def qr(self, data):
        return self.req('qr', data)
