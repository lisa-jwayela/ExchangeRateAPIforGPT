# Import the needed libraries
import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv
from flask import Flask, request

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(dotenv_path=BASE_DIR / ".env", override=False)

# Initialize the Flask app
app = Flask(__name__)

# API used to get exchange rates for GBP to ZAR
# Documentation: https://www.exchangerate-api.com/docs/python-currency-api
EXCHANGE_RATE_URL = "https://v6.exchangerate-api.com/v6/"
ERROR_STRING = "The authorization header is missing a Bearer token key or doesn't match the required key."  # pragma: allowlist secret
MISSING_KEY_STRING = (
    "Missing EXCHANGE_RATE_API_KEY environment variable."  # pragma: allowlist secret
)
MISSING_SERVICE_KEY_STRING = (
    "Missing SERVICE_AUTH_KEY environment variable."  # pragma: allowlist secret
)


def get_api_key():
    return os.getenv("EXCHANGE_RATE_API_KEY")


def get_service_auth_key():
    return os.getenv("SERVICE_AUTH_KEY")


# Requires token be present
def assert_auth_header():
    service_auth_key = get_service_auth_key()
    if not service_auth_key:
        raise ValueError(MISSING_SERVICE_KEY_STRING)
    auth_header = request.headers.get("Authorization", None)
    if auth_header != f"Bearer {service_auth_key}":
        raise AssertionError(ERROR_STRING)


# Default route populated to show things are working when we deploy and test
@app.route("/")
def index():
    return "Health Check: Your exchange rate API plugin is working"


# This route contains the core functionality to get todays exchange rate for GBP to ZAR and return it as a number
# Local test: http://127.0.0.1:5000/GBPRate``


@app.route("/GBPRate", methods=["GET"])
def get_gbp_rate():
    try:
        api_key = get_api_key()
        if not api_key:
            return MISSING_KEY_STRING, 500
        assert_auth_header()
        response = requests.get(f"{EXCHANGE_RATE_URL}{api_key}/latest/GBP", timeout=10)
        api_data = response.json()
        exchange_rate_for_GBP_to_rand = api_data["conversion_rates"]["ZAR"]
        return str(exchange_rate_for_GBP_to_rand)
    except AssertionError:
        return ERROR_STRING, 401
    except ValueError as e:
        return str(e), 500
    except requests.Timeout:
        return "The exchange rate API request timed out. Please try again later.", 504
    except requests.RequestException as e:
        return f"Failed to reach the exchange rate API: {e}", 502
    except (KeyError, json.JSONDecodeError) as e:
        return f"Unexpected response from the exchange rate API: {e}", 502


# This route contains the core functionality to get todays exchange rate for USD to ZAR and return it as a number
# Local test: http://127.0.0.1:5000/USDRate


@app.route("/USDRate", methods=["GET"])
def get_usd_rate():
    try:
        api_key = get_api_key()
        if not api_key:
            return MISSING_KEY_STRING, 500
        assert_auth_header()
        response = requests.get(f"{EXCHANGE_RATE_URL}{api_key}/latest/USD", timeout=10)
        api_data = response.json()
        exchange_rate_for_USD_to_rand = api_data["conversion_rates"]["ZAR"]
        return str(exchange_rate_for_USD_to_rand)
    except AssertionError:
        return ERROR_STRING, 401
    except ValueError as e:
        return str(e), 500
    except requests.Timeout:
        return "The exchange rate API request timed out. Please try again later.", 504
    except requests.RequestException as e:
        return f"Failed to reach the exchange rate API: {e}", 502
    except (KeyError, json.JSONDecodeError) as e:
        return f"Unexpected response from the exchange rate API: {e}", 502
