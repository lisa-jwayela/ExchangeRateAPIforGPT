# Creating GPT with Actions that calls API
Simple API to use with a Custom GPT to demonstrate how it can perform actions to get Pound exchange rate for the day

## API using
https://v6.exchangerate-api.com/v6/ for exchange rates


## Setup Virtual Env and test API in Jupyter Notebook

NOTE: Make a virtual environment for python v3.14 t

And then use VS Notebook: Select Notebook Kernel to select the virtual environment to test with Jupyter Notebook

## How to run in Flask

In terminal
```console
cd C:\LisaData\Code\GPTs\ExchangeRateAPIforGPT

python -m venv .venv
.venv\Scripts\Activate.ps1 

python.exe -m pip install --upgrade pip 

pip install flask requests

$env:FLASK_APP = "plugin.py"
$env:FLASK_ENV = "development"

flask --app plugin run

```
 API will be available at http://127.0.0.1:5000/ using browser or Postman


### Python anywhere for testing web service api
https://lisajwa.pythonanywhere.com should give default message that API running

Must put plugin.py and openapi.yaml as files on https://www.pythonanywhere.com


### Ideas for Instructions for Custom GPT
You are giving feedback to user about the British pound (GBP) and/or the dollar (USD) exchange rates to South African rands (ZAR) for today using the Actions API.  
users want to understand what the trends are for these 2 exchange rates. While always use the Actions API to get accurate exchange rates, use the web for other questions from the user.
Share with them past year and last months trends. Also share expected exchange rate in the next week and research this on web to give useful research insights

#### Notes for Action

Must add action with SERVICE_AUTH_KEY for bearer authentication