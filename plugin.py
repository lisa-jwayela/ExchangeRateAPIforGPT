#Import the needed libraries
import os
import requests
from flask import Flask, request

#Initialize the Flask app
app = Flask(__name__)

# API used to get exchange rates for GBP to ZAR
# Documentation: https://www.exchangerate-api.com/docs/python-currency-api
EXCHANGE_RATE_URL = "https://v6.exchangerate-api.com/v6/"
API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")
SERVICE_AUTH_KEY = os.getenv("SERVICE_AUTH_KEY")
ERROR_STRING = "The authorization header is missing a Bearer token key or doesn't match the required key."
MISSING_KEY_STRING = "Missing EXCHANGE_RATE_API_KEY or SERVICE_AUTH_KEY environment variable."

# Requires token be present
def assert_auth_header():
  if not SERVICE_AUTH_KEY:
    raise ValueError(MISSING_KEY_STRING)
  auth_header = request.headers.get("Authorization", None)
  if auth_header != f"Bearer {SERVICE_AUTH_KEY}":
    raise AssertionError(ERROR_STRING)


# Default route populated to show things are working when we deploy and test
@app.route("/")
def index():
    return "Your exchange rate api plugin is working"

# This route contains the core functionality to get todays exchange rate for GBP to ZAR and return it as a number
# Local test: http://127.0.0.1:5000/GBPRate``

@app.route('/GBPRate', methods=['GET'])
def get_gbp_rate():
  try:
    if not API_KEY:
      return MISSING_KEY_STRING, 500
    assert_auth_header()
    response = requests.get(EXCHANGE_RATE_URL + API_KEY + "/latest/GBP")
    api_data = response.json()
    exchange_rate_for_GBP_to_rand = api_data["conversion_rates"]["ZAR"]
    return str(exchange_rate_for_GBP_to_rand)
  except AssertionError:
     return ERROR_STRING, 401
  except ValueError as e:
    return str(e), 500
  except:
    return "The exchange rate API is currently down. You may have a bug. Please try your request again later."

# This route contains the core functionality to get todays exchange rate for USD to ZAR and return it as a number
# Local test: http://127.0.0.1:5000/USDRate

@app.route('/USDRate', methods=['GET'])
def get_usd_rate():
  try:
    if not API_KEY:
      return MISSING_KEY_STRING, 500
    assert_auth_header()
    response = requests.get(EXCHANGE_RATE_URL + API_KEY + "/latest/USD")
    api_data = response.json()
    exchange_rate_for_USD_to_rand = api_data["conversion_rates"]["ZAR"]
    return str(exchange_rate_for_USD_to_rand)
  except AssertionError:
     return ERROR_STRING, 401
  except ValueError as e:
    return str(e), 500
  except:
    return "The exchange rate API is currently down. You may have a bug. Please try your request again later."


