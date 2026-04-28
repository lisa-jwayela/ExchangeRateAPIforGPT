# Testing the Exchange Rate API for GPT Actions

Multiple ways to test:
1. Directly to the 3rd party [Exchange Rate API using Jupyter Notebook](#1-provider-integration-test-jupyter-notebook)
2. Against locally running [Flask web app API](#2-local-web-app-api-test-with-postman) using Postman
3. Against cloud hosted [web app API running on PythonAnywhere](#3-api-client-test-with-pythonanywhere)
4. Testing a GPT Action using the openAPI schema. See [GPT Action setup notes](#gpt-action-setup)

## 1) Provider integration test Jupyter notebook

`test-exchange-rate-api.ipynb` calls ExchangeRate-API directly.

Required environment variable:

```console
setx EXCHANGE_RATE_API_KEY "your_exchange_rate_api_key"
```

If you use `setx`, restart VS Code before running notebook cells.

## 2) Local web app API test with Postman

```console

$env:EXCHANGE_RATE_API_KEY = "your_exchange_rate_api_key" # pragma: allowlist secret
$env:SERVICE_AUTH_KEY = "your_service_auth_key" # pragma: allowlist secret

$env:FLASK_APP = "plugin.py"
$env:FLASK_ENV = "development"

# Run the plugin in Flask locally
flask --app plugin run
```

Health check URL against locally running Flask web-based API:
```text
http://127.0.0.1:5000/
```

URLs for testing with Postman

- `http://127.0.0.1:5000/`
- `http://127.0.0.1:5000/GBPRate`
- `http://127.0.0.1:5000/USDRate`

Include `Authorization: Bearer <SERVICE_AUTH_KEY>` for protected endpoints.

## 3) API client test with PythonAnywhere

1. Login to your PythonAnywhere account
2. Follow these instructions for Flask on Python: https://help.pythonanywhere.com/pages/Flask

3. Then upload these files for the "mysite" folder:
- plugin.py and
- openapi.yaml
- .env

In a PythonAnywhere Bash console, install the required packages:

```console
pip install flask requests python-dotenv
```

### 3.1 Test with Juypter Notebook
`test-exchange-rate-plugin.ipnb`

### 3.2 Test with Postman

Use Postman to call:

- `https://<your-pythonanywhere-domain>/`
- `https://<your-pythonanywhere-domain>/GBPRate`
- `https://<your-pythonanywhere-domain>/USDRate`

Include `Authorization: Bearer <SERVICE_AUTH_KEY>` for protected endpoints.

## GPT Action Setup

Reference: https://help.openai.com/en/articles/8770868-gpt-builder

Use `openapi.yaml` as the action schema and configure Bearer authentication with `SERVICE_AUTH_KEY`.

### POC Prompt/Instructions for GPT Action
You are a currency insights assistant focused on GBP/ZAR and USD/ZAR.

Primary behavior:

You are a GBP/ZAR and USD/ZAR currency insights assistant.

For current rates, always call the Actions API first.
Show the current rate(s) with retrieval date/time.
1) Explain movement in clear, non-technical language.
2) Use credible web sources for past month/year context and 1-week outlook.
3) Clearly label what comes from:
- Actions API
- Web research
- Your interpretation

If API fails:

1) Say the API is unavailable.
2) Provide best-effort web-based context.
3) Note reduced confidence.

Style:

Keep responses concise and executive-friendly.
Do not give financial advice.
Ask one clarifying question only if user intent is unclear.

Default response structure:

1) Current snapshot
2) Trend context (1 month, 1 year)
3) 1-week outlook
4) Key risks/watchouts
5) Source note (API timestamp + web sources used)
