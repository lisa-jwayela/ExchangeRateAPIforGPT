# Creating GPT with Actions that calls API


## API using
https://v6.exchangerate-api.com/v6/ for exchange rates



## Lisa Notes
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
https://lisajwa.pythonanywhere.com