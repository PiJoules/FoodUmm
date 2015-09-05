import private
from urllib import urlencode
from urllib2 import Request, urlopen
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
	foodTypes = menu["menu"]
	foodType = foodTypes[random.randint(0,len(foodTypes)-1)]
	print foodType["name"]

	foodItems = foodType["children"]
	return foodItems[random.randint(0,len(foodItems)-1)]


	print json.dumps(menu,sort_keys=True,indent=4, separators=(',', ': '))
	print "dank memes"

if __name__ == '__main__':
	# test code pls ignore
	options = search("3141 Chestnut St, Philadelphia, PA 19104")
	merchantId = pickRestaurant(options)
	menu = getMenu(merchantId)
	food = pickItem(menu)
	print food["name"]