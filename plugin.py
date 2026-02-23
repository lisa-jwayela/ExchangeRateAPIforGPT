#Import the needed libraries
import requests
import json
from flask import Flask, request, send_from_directory
from datetime import datetime

#Initialize the Flask app
app = Flask(__name__)

# API used to get exchange rates for GBP to ZAR
# Documentation: https://www.exchangerate-api.com/docs/python-currency-api
EXCHANGE_RATE_URL = "https://v6.exchangerate-api.com/v6/"
API_KEY = "529d3453809b9ec1e660421b" 
SERVICE_AUTH_KEY = "3987598723758730397456"
ERROR_STRING = "The authorization header is missing a Bearer token key or doesn't match the required key."

# Requires token be present
def assert_auth_header():
    assert request.headers.get(
        "Authorization", None) == f"Bearer {SERVICE_AUTH_KEY}"


# Default route populated to show things are working when we deploy and test
@app.route("/")
def index():
    return "Your exchange rate api plugin is working"

# This route contains the core functionality to get todays exchange rate for GBP to ZAR and return it as a number
# Local test: http://127.0.0.1:5000/GBPRate``

@app.route('/GBPRate', methods=['GET'])
def get_gbp_rate():
  try:
    assert_auth_header()
    response = requests.get(EXCHANGE_RATE_URL + API_KEY + "/latest/GBP")
    api_data = response.json()
    exchange_rate_for_GBP_to_rand = api_data["conversion_rates"]["ZAR"]
    return str(exchange_rate_for_GBP_to_rand)
  except AssertionError:
     return ERROR_STRING
  except:
    return "The exchange rate API is currently down. You may have a bug. Please try your request again later."


