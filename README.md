# API to use for GPT with Custom Actions that calls this API
Simple API to use with a OpenAI GPT Actions to demonstrate getting Pound and $ exchange rate for the day

## API using
https://v6.exchangerate-api.com/v6/ for exchange rates


## Getting Started
Prerequisites

- Python 3.14 (recommended)
- https://pypi.org/project/Flask/
- Jupyter Notebook for testing 3rd party APIs
- Account for https://chatgpt.com/gpts 
  
### Setup Virtual Env and test API in Jupyter Notebook

NOTE: Make a virtual environment for python v3.14 t
And then use VS "Notebook: Select Notebook Kernel" to select the virtual environment to test with Jupyter Notebook

In terminal
```console
cd C:\LisaData\Code\GPTs\ExchangeRateAPIforGPT

python -m venv .venv
.venv\Scripts\Activate.ps1 

python.exe -m pip install --upgrade pip 
```

### Setup Flask to run the API for testing locally

```console
pip install flask requests

$env:FLASK_APP = "plugin.py"
$env:FLASK_ENV = "development"

flask --app plugin run
```
 API will be available at http://127.0.0.1:5000/ 
 For testing with browser to test default endpoint

## Setup PythonAnywhere for testing API in cloud
Go to  https://www.pythonanywhere.com
Create free account
Upload these 2 files for the "mysite" folder: plugin.py and openapi.yaml 

Then use Postman for https://lisajwa.pythonanywhere.com and see default message that API running
Then use Postman for testing https://lisajwa.pythonanywhere.com/GBPRate or 
https://lisajwa.pythonanywhere.com/USDRate with Bearer token authorization to see rates

Can also use TestCurrencyPlugin Jupyter Notebook

## Setup GPTBuilder for ChatGPT
https://help.openai.com/en/articles/8770868-gpt-builder

### Ideas for Instructions for Custom GPT
You are giving feedback to user about the British pound (GBP) and/or the dollar (USD) exchange rates to South African rands (ZAR) for today using the Actions API.  
users want to understand what the trends are for these 2 exchange rates. While always use the Actions API to get accurate exchange rates, use the web for other questions from the user.
Share with them past year and last months trends. Also share expected exchange rate in the next week and research this on web to give useful research insights

#### Notes for Action

Must add action with SERVICE_AUTH_KEY for bearer authentication