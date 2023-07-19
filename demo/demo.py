from FixedFloatApi import FixedFloatApi
import os

api = FixedFloatApi(os.getenv("FF_API_KEY"),os.getenv("FF_SECRET_KEY"))

# Get all currencies:
#print(api.ccies())

# Create exchange order:
order_data = {
    "fromCcy": "ETH",
    "toCcy": "BTC",
    "amount": 0.5,
    "direction": "from",
    "type": "fixed",
    "toAddress": "bc1q3c5ppjxwkkuuqdpnlnkxdfegyyu7mfdn8dxaxp"
}
#print(api.create(order_data))

# Get order:
order_info = {"id": "AA3SDU", "token": "c5agWZ24zRL7An4sIstIJTdVcvwgG1jPeC5Uadwc"} 
#print(api.order(order_info))


# Get pair exchange price:
price_data = {
    "fromCcy": "BTC",
    "toCcy": "MATICETH",
    "amount": 0.5,
    "direction": "from",
    "type": "fixed"
}
print(api.price(price_data))

# Setting emergency:
#emergency_data = {"id": "AA3SDU", "token": "c5agWZ24zRL7An4sIstIJTdVcvwgG1jPeC5Uadwc", "choice": "EXCHANGE"}
#print(api.emergency(emergency_data))

# Set email:
email_data = {"id": "AA3SDU", "token": "c5agWZ24zRL7An4sIstIJTdVcvwgG1jPeC5Uadwc", "email": "fsgdffg@gmail.com"}
#print(api.setEmail(email_data))

# Generate QR code:
qr_data = {"id": "AA3SDU", "token": "c5agWZ24zRL7An4sIstIJTdVcvwgG1jPeC5Uadwc"}
#print(api.qr(qr_data))
 