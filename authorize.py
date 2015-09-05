import private
from urllib import urlencode
from urllib2 import Request, urlopen, URLError
import json
import random
import requests

def get_tokens(base, auth_code, refresh_token=None):
	payload = {
		"client_id": private.delivery_client_id,
		"redirect_uri": private.delivery_redirect_uri,
		"grant_type": "authorization_code",
		"client_secret": private.delivery_client_secret,
		"code": auth_code
	}
	if refresh_token:
		payload["refresh_token"] = refresh_token
	url = base + "/third_party/access_token"
	req = Request(url, urlencode(payload))
	resp = urlopen(req)
	text = resp.read()
	resp.close()
	resp = json.loads(text)
	return {
		"access_token": resp["access_token"],
		"refresh_token": resp["refresh_token"]
	}

"""
Retrieve guest token for adding stuff to cart
https://developers.delivery.com/customer-cart/
"""
def get_guest_token(base, client_id):
	payload = {
		"client_id": client_id
	}
	url = base + "/customer/auth/guest?" + urlencode(payload)
	req = Request(url)
	resp = urlopen(req)
	text = resp.read()
	resp.close()
	return json.loads(text)["Guest-Token"]

"""
Merchant serach from address (delivery)
https://developers.delivery.com/merchant-search/
"""
def search(base, address, client_id, method="delivery"):
	payload = {
		"address": address,
		"client_id": client_id,
		"merchant_type": "R"
	}
	url = base + "/merchant/search/" + method + "?" + urlencode(payload)
	req = Request(url)
	resp = urlopen(req)
	text = resp.read()
	resp.close()
	return json.loads(text)

"""
Get a random restaurant (ID)
"""
def rand_merchant(merchants):
	return random.choice(merchants["merchants"])

"""
Get menu from merchant id
https://developers.delivery.com/merchant-menu/
"""
def get_menu(base, merchant_id, client_id):
	payload = {
		"client_id": client_id,
		"item_only": 1,
		"hide_unavailable": 1
	}
	url = base + "/merchant/" + merchant_id + "/menu?" + urlencode(payload)
	req = Request(url)
	resp = urlopen(req)
	text = resp.read()
	resp.close()
	return json.loads(text)

"""
Add a random item from the menu

A message like this should be returned if successful:
{
  "message": [
 
  ],
  "subtotal": 9,
  "tax": 0.8,
  "item_key": 0,
  "item_count": 1,
  "order_time": "2014-02-07T18:30:00-0500"
}
"""
def add_item(base, token, inventory, merchant_id, client_id, order_type="delivery", order_qty=1):
	# Find a random item
	menus = inventory["menu"]
	food_type = random.choice(menus)
	selection = random.choice(food_type["children"])
	food_id = selection["id"]

	# Add the item
	url = base + "/customer/cart/" + merchant_id + "?" + urlencode({"client_id": client_id})
	payload = {
		"order_type": order_type,
		"instructions": "",
		"item": {
			"item_id": food_id,
			"item_qty": order_qty
		},
		"client_id": client_id,
	}
	headers = {
		"Guest-Token": token,
		'Content-type': 'application/json'
	}
	r = requests.post(url, data=json.dumps(payload), headers=headers)
	print r.status_code, r.reason
	return r.json()