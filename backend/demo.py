from fixedfloat.fixedfloat import FixedFloat

api = FixedFloat("111","111")

# Get all currencies:
print(api.get_currencies())

# Create exchange order:

test_btc_address = "1MDDHnGntLetTsgiuahSx66Q6Mje8xNftN"
order = api.create_order("ETH", "BTC", 0.5, test_btc_address, "fixed")
print(order)

# Get order:

print(api.get_order("ORDER_ID", "TOKEN")) # you can get TOKEN after creating an order

# Get pair exchange price:

print(api.get_price("ETH", 0.5, "BTC", "fixed"))

# Setting emergency:

print(api.set_emergency("ORDER_ID", "TOKEN", "EXCHANGE"))