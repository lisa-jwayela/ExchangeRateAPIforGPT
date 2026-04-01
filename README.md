# REST API for GPT Custom Actions
Simple Flask API designed for OpenAI GPT Actions to return daily GBP->ZAR and USD->ZAR exchange rates.

## Getting Started
Prerequisites

- Python 3.14 (recommended)
- Python's Flask lightweight framework for building REST APIs https://pypi.org/project/Flask/
- Key to use free API for currency conversion rates for 165 currencies https://v6.exchangerate-api.com
- Account for creating a Custom GPT Action https://chatgpt.com/gpts 
- Jupyter Notebook for testing
- Create free account https://www.pythonanywhere.com for testing as a webservice
Create free account
  
### Setup Virtual Env, Jupyter Notebook and Flask

Assume Windows and Visual Studio Code
1) Make a virtual environment for python v3.14
2) And then use VS "Notebook: Select Notebook Kernel" to select the virtual environment for the Jupyter Notebook
3) Execute commands below

```console
python -m venv .venv
.venv\Scripts\Activate.ps1 

python.exe -m pip install --upgrade pip 

pip install flask requests

$env:EXCHANGE_RATE_API_KEY = "your_exchange_rate_api_key"
$env:SERVICE_AUTH_KEY = "your_service_auth_key"

$env:FLASK_APP = "plugin.py"
$env:FLASK_ENV = "development"

flask --app plugin run
```
## Testing 
### Test Locally using Flask, Postman and/or Jupyter Notebooks
 
 #### 1) With Flask 
 REST API will be available at http://127.0.0.1:5000/ for the health check on default endpoint

#### 2) Jupyter Notebook 
```console
setx EXCHANGE_RATE_API_KEY "your_exchange_rate_api_key"
setx SERVICE_AUTH_KEY "your_service_auth_key"
# Restart Visual Studio before using Notebook
```
- `TestCurrencyAPI.ipynb` calls the third-party ExchangeRate-API directly (ie integration sanity check).

### Test hosted in cloud with Authentication

Login to your PythonAnywhere account and upload these 2 files for the "mysite" folder: 
- plugin.py and 
- openapi.yaml 

#### 1) Use Postman for testing 
Replacing the URL with your pythonanywhere URL
1) https://lisajwa.pythonanywhere.com and see default message that API running
2) https://lisajwa.pythonanywhere.com/GBPRate or
https://lisajwa.pythonanywhere.com/USDRate with Bearer token authorization to see todays exchange rates.

#### 2) Jupyter Notebook 
```console
setx EXCHANGE_RATE_API_KEY "your_exchange_rate_api_key"
setx SERVICE_AUTH_KEY "your_service_auth_key"
# Restart Visual Studio before using Notebook
```
- `TestCurrencyPlugin.ipynb` calls this project API running on PythonAnywhere using Bearer authentication (see details below).


## API Design

### Bearer Token Authentication

The `/GBPRate` and `/USDRate` endpoints are protected with HTTP Bearer token authentication. 

- **Supports GPT Actions** – OpenAI's GPT Actions framework requires Bearer auth for API integrations
- **Environment-based key management** – The `SERVICE_AUTH_KEY` is loaded from environment variables, keeping secrets out of source code

**Request format:**
```
GET /GBPRate
Authorization: Bearer <SERVICE_AUTH_KEY>
```

**Response on auth failure:**
```
401 Unauthorized
"The authorization header is missing a Bearer token key or doesn't match the required key."
```

### OpenAPI Specification

The `openapi.yaml` file formally documents the API contract using OpenAPI 3.1.0 standard. This enables:

- **GPT Action integration** – OpenAI reads the OpenAPI spec to understand endpoints, parameters, and authentication
- **API discoverability** – So can use Postman to test
- **Security declaration** – The `securitySchemes` section explicitly defines Bearer auth requirements


## Setup GPTBuilder for ChatGPT
https://help.openai.com/en/articles/8770868-gpt-builder

### Ideas for Instructions for Custom GPT
You are giving feedback to user about the British pound (GBP) and/or the dollar (USD) exchange rates to South African rands (ZAR) for today using the Actions API.  
users want to understand what the trends are for these 2 exchange rates. While always use the Actions API to get accurate exchange rates, use the web for other questions from the user.
Share with them past year and last months trends. Also share expected exchange rate in the next week and research this on web to give useful research insights

#### Notes for Action

Set Bearer authentication using `SERVICE_AUTH_KEY`.