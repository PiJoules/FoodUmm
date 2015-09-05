import private
from urllib import urlencode
from urllib2 import Request, urlopen, URLError, HTTPError
import json
import random

def search(address):
	payload = {
		"address": address,
		"client_id": private.delivery_client_id
	}
	url = "http://sandbox.delivery.com/merchant/search/delivery?" + urlencode(payload)
	request = Request(url)
	response = urlopen(request)
	text = response.read()
	response.close()
	return json.loads(text)

def pickRestaurant(options):
	restaurants = options["merchants"]
	restaurant = restaurants[random.randint(0,len(restaurants)-1)]
	print restaurant["summary"]["name"]
	return restaurant["id"]

def getMenu(merchantId):
	payload = {
		"hide_unavailable": 1,
		"client_id": private.delivery_client_id
	}
	url = "http://sandbox.delivery.com/merchant/" + merchantId + "/menu?" + urlencode(payload)
	request = Request(url)
	response = urlopen(request)
	text = response.read()
	response.close()
	return json.loads(text)

def pickItem(menu):
	# Traverse menus and pick one at random
	menu = menu["menu"]
	while "children" in menu:
		menu = menu["children"]
	foodItem = menu[random.randint(0,len(menu)-1)]
	print foodItem["name"]

	# Pick an item
	while "children" in foodItem and len(foodItem["children"]) > 0:
		foodItems = foodItem["children"]
		foodItem = foodItems[random.randint(0,len(foodItems)-1)]
		if foodItem["type"] == "item":
			break
	optionsDict = {}
	for optionsGroup in foodItem["children"]:
		options = optionsGroup["children"]
		option = options[random.randint(0,len(options)-1)]
		optionsDict[option["id"]] = 1

	return (foodItem, optionsDict)

def addItem(merchantId, item, options, token):
	payload = {
		"order_type": "delivery",
		"item": {
			"item_id": item["id"],
			"item_qty": 1,
  			"option_qty": options
		},
		"client_id": private.delivery_client_id
	}
	header = {"Guest-Token": token}
	url = "http://sandbox.delivery.com/customer/cart/" + merchantId
	request = Request(url, urlencode(payload), header)
	try:
		response = urlopen(request)
		text = response.read()
		response.close()
		return json.loads(text)
	except HTTPError as e:
		print "HTTP Error: " + e.reason
		print e.read()
	except URLError as e:
		print "URL Error: " + e.code
		print e.reason
	return {}

def checkCart(merchantId, address, token):
	payload = {
		"order_type": "delivery",
		"client_id": private.delivery_client_id,
		"zip": address["zip_code"],
		"city": address["city"],
		"state": address["state"],
		"latitude": address["latitude"],
		"longitude": address["longitude"]
	}
	header = {"Guest-Token": token}
	url = "http://sandbox.delivery.com/customer/cart/" + merchantId + "/?" + urlencode(payload)
	request = Request(url, headers=header)
	response = urlopen(request)
	text = response.read()
	response.close()
	return json.loads(text)

def getToken():
	payload = {
		"client_id": private.delivery_client_id
	}
	url = "http://sandbox.delivery.com/customer/auth/guest/?" + urlencode(payload)
	request = Request(url)
	response = urlopen(request)
	text = response.read()
	response.close()
	return json.loads(text)["Guest-Token"]

if __name__ == '__main__':
	# test code pls ignore
	options = search("3141 Chestnut St, Philadelphia, PA 19104")
	address = options["search_address"]
	merchantId = pickRestaurant(options)
	menu = getMenu(merchantId)
	(food, itemOptions) = pickItem(menu)
	print "Options: " + json.dumps(itemOptions,sort_keys=True,indent=4, separators=(',', ': '))
	print json.dumps(food,sort_keys=True,indent=4, separators=(',', ': '))
	print food["name"]
	print food["id"]

	# Make guest token so order can be submitted
	token = getToken()
	cart = checkCart(merchantId, address, token)
	items = addItem(merchantId, food, itemOptions, token)
	print json.dumps(items,sort_keys=True,indent=4, separators=(',', ': '))
