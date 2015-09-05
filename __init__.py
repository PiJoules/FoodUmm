
import vendor
vendor.add('lib')

# Import the Flask Framework
from flask import Flask, render_template, jsonify, request, url_for
app = Flask(__name__)

import private
from urllib import urlencode
from urllib2 import Request, urlopen
import json

@app.route("/")
def index_route():
	return render_template("index.html", poop="poopkksjdn")

@app.route("/test")
def test_route():
	payload = {
		"address": "3141 Chestnut St, Philadelphia, PA 19104",
		"client_id": private.delivery_client_id
	}
	url = "http://sandbox.delivery.com/merchant/search/delivery?" + urlencode(payload)
	request = Request(url)
	response = urlopen(request)
	text = response.read()
	response.close()
	return jsonify(response=json.loads(text))

@app.route("/redirect")
def redirect_route():
	return render_template("redirect.html")

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