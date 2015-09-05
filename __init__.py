
import vendor
vendor.add('lib')

# Import the Flask Framework
from flask import Flask, render_template, jsonify, request, url_for, redirect
app = Flask(__name__)

import private
from urllib import urlencode
from urllib2 import Request, urlopen
import json

base = "http://sandbox.delivery.com"

@app.route("/")
def index_route():
	return render_template("index.html", poop="poopkksjdn")

@app.route("/test")
def test_route(address="3141 Chestnut St, Philadelphia, PA 19104"):
	payload = {
		"address": address,
		"client_id": private.delivery_client_id
	}
	url = base + "/merchant/search/delivery?" + urlencode(payload)
	req = Request(url)
	resp = urlopen(req)
	text = resp.read()
	resp.close()
	return jsonify(response=json.loads(text))

@app.route("/login")
def login_route():
	payload = {
		"client_id": private.delivery_client_id,
		"redirect_uri": private.delivery_redirect_uri,
		"response_type": "code",
		"scope": "global",
		"state": "login"
	}
	url = base + "/third_party/authorize?" + urlencode(payload)
	return redirect(url)

@app.route("/payment")
def payment_route():
	payload = {
		"client_id": private.delivery_client_id,
		"redirect_uri": private.delivery_redirect_uri,
		"response_type": "code",
		"scope": "global",
		"state": "payment"
	}
	return redirect(base + "/third_party/credit_card/add?" + urlencode(payload))

@app.route("/paymethods")
def payment_types_route():
	url = base + "/customer/cc"
	req = Request(url)
	resp = urlopen(req)
	text = resp.read()
	resp.close()
	return jsonify(resp=text)

@app.route("/redirect")
def redirect_route():
	# Params for login
	error = request.args.get("error")
	state = request.args.get("state")
	code = request.args.get("code")
	if error:
		return jsonify(error=error, state=state, message="login failed")
	elif code:
		return jsonify(code=code, state=state, message="login success")
	else:
		return jsonify(error=error, code=code, state=state, message="I have no idea what happened")

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