
import vendor
vendor.add('lib')

# Import the Flask Framework
from flask import Flask, render_template, jsonify, request, url_for, redirect
app = Flask(__name__)

import private
from urllib import urlencode
from urllib2 import Request, urlopen
import json
from authorize import get_tokens

base = "http://sandbox.delivery.com"

@app.route("/")
def index_route():
	authorization_code = request.args.get("ac")
	if authorization_code:
		logged_in = True
	else:
		logged_in = False
	return render_template("index.html", logged_in=logged_in)

@app.route("/login")
def login_route():
	# state = request.args.get("s")
	# access_token = request.args.get("at")
	# authorization_code = request.args.get("ac")
	# refresh_token = request.args.get("rt")
	# if not state:
	# 	state = "/"
	# payload = {
	# 	"client_id": private.delivery_client_id,
	# 	"redirect_uri": private.delivery_redirect_uri,
	# 	"response_type": "code",
	# 	"scope": "global",
	# 	"state": state
	# }
	# url = base + "/third_party/authorize?" + urlencode(payload)
	# return redirect(url)
	redirect_uri = request.args.get("ru")
	if not redirect_uri:
		redirect_uri = "/"
	return render_template("login.html", redirect_uri=redirect_uri)

@app.route("/logout")
def logout_route():
	# redirect_uri = request.args.get("ru")
	# if not redirect_uri:
	# 	redirect_uri = "/"
	# payload = {
	# 	"redirect_uri": redirect_uri,
	# 	"client_id": private.delivery_client_id
	# }
	# delivery_logout_url = base + "/yelp-api/third_party/authorize/logout?%2Fthird_party%2Fauthorize=&scope=global&state=%2F&response_type=code&" + urlencode(payload)
	# return redirect(delivery_redirect_uri)
	redirect_uri = request.args.get("ru")
	if not redirect_uri:
		redirect_uri = "/"
	return render_template("logout.html", redirect_uri=redirect_uri)

@app.route("/payment")
def payment_route():
	payload = {
		"client_id": private.delivery_client_id,
		"redirect_uri": private.delivery_redirect_uri_base,
		"response_type": "code",
		"scope": "global",
		"state": "payment"
	}
	return redirect(base + "/third_party/credit_card/add?" + urlencode(payload))

@app.route("/paymethods")
def payment_types_route():
	access_token = request.args.get("at")
	authorization_code = request.args.get("ac")
	refresh_token = request.args.get("rt")
	if access_token: # Logged in and authorized
		url = base + "/customer/cc"
		req = Request(url)
		req.add_header("Authorization", access_token)
		resp = urlopen(req)
		text = resp.read()
		resp.close()
		return jsonify(resp=json.loads(text))
	elif authorization_code or refresh_token: # Logged in but no ref token
		tokens = get_tokens(base, authorization_code, refresh_token)
		url = base + "/customer/cc"
		req = Request(url)
		req.add_header("Authorization", tokens["access_token"])
		resp = urlopen(req)
		text = resp.read()
		resp.close()
		return jsonify(resp=json.loads(text))
	else: # Not logged in
		return redirect("/login?" + urlencode({"s":"/paymethods"})) # Login and return back to this page

@app.route("/redirect")
def redirect_route():
	# Params for login
	error = request.args.get("error")
	state = request.args.get("state") # The URL to redirect back to after getting auth code
	code = request.args.get("code") # authorization_code
	if error:
		return jsonify(error=error, state=state, message="login failed")
	elif code:
		tokens = get_tokens(base, code)
		return redirect(state + "?" + urlencode({
			"at": tokens["access_token"],
			"ac": code,
			"rt": tokens["refresh_token"]
		}))
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