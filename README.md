# Creating GPT with Actions that calls API
Simple API to use with a Custom GPT to demonstrate how it can perform actions to get Pound exchange rate for the day

## API using
https://v6.exchangerate-api.com/v6/ for exchange rates



## How to run in Flask
In terminal
cd C:\Lisa Files and Data\3-Work\2025\Code\GPTs\<projectname>

python -m venv venv
.\venv\Scripts\activate

pip install flask requests

$env:FLASK_APP = "plugin.py"
$env:FLASK_ENV = "development"

flask --app plugin run

 API will be available at http://127.0.0.1:5000/ using browser or Postman


### Python anywhere for testing web service api
https://lisajwa.pythonanywhere.com should give default message that API running

Must put plugin.py and openapi.yaml as files on https://www.pythonanywhere.com


### Ideas for Instructions for Custom GPT
You are giving feedback to users about the british pound (GBP) to south african rands (ZAR) exchange rate.  Users want to understand what the trends are for this particular exchange rate. Share with them trends and expected exchange rate in the next week. Limit text out put to 6 sentences to keep it short

Must add action with SERVICE_AUTH_KEY for bearer authentication