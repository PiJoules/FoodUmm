
import vendor
vendor.add('lib')

# Import the Flask Framework
from flask import Flask, render_template, jsonify, request, url_for, redirect
app = Flask(__name__)

import private
from urllib import urlencode
from urllib2 import Request, urlopen
import json
import authorize

base = "http://sandbox.delivery.com"
client_id = private.delivery_client_id
redirect_uri = private.delivery_redirect_uri
url_to_add_cc_in_browser = base + "/third_party/credit_card/add?client_id=" + client_id + "&redirect_uri=" + redirect_uri + "&response_type=code&scope=global"

@app.route("/")
def index_route():
	return render_template("index.html")

@app.route("/search")
def search_route():
	guest_token = authorize.get_guest_token(base, client_id)
	address = request.args.get("address")
	merchant_info = authorize.search(base, address, client_id)
	rand_merchant = authorize.rand_merchant(merchant_info)
	menu = authorize.get_menu(base, rand_merchant["id"], client_id)
	# print menu
	add_item_resp = authorize.add_item(base, guest_token, menu, rand_merchant["id"], client_id)
	return jsonify(item_resp=add_item_resp)

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500

if __name__ == "__main__":
	app.run()