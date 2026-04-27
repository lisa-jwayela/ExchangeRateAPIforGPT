# Exchange Rate API for GPT Actions

This POC project is a lightweight REST API that exposes two focused currency endpoints for use in a GPT Action:

- GBP to ZAR
- USD to ZAR

It is used to demonstrate a custom GPT Action calling an API for OpenAI GPT Actions and for Dimagi Open Chat Studio Custom Actions (https://github.com/dimagi/open-chat-studio)

## What This Project Demonstrates

- Design: wraps a third-party exchange-rate provider behind an internal API.
- OpenAPI 3.1 specification for GPT Action compatibility.
- Security: protected endpoints with HTTP Bearer token.
- Easy deployment: hosted verification path on PythonAnywhere.
- Testing layers: separate notebook flows for provider-level checks and wrapper API checks.

## Architecture Overview

1. A Flask API receives client requests.
2. The API validates the Bearer token for protected endpoints.
3. The service calls ExchangeRate-API as an upstream provider.
4. The service returns the ZAR exchange rate value as plain text.

### Why plain-text responses?

For this POC, returning a plain text value keeps the API simple for GPT Actions and quick manual tests.

## API Surface

- `GET /` health check endpoint.
- `GET /GBPRate` returns latest GBP to ZAR exchange rate (requires Bearer token).
- `GET /USDRate` returns latest USD to ZAR exchange rate (requires Bearer token).

## Authentication Design

The `/GBPRate` and `/USDRate` endpoints use HTTP Bearer token authentication.

- This is a deliberate security design for testing how GPT Actions handle security
- GPT Actions can work with this pattern when configured via OpenAPI.
- `SERVICE_AUTH_KEY` is loaded from environment variables, not hardcoded secrets.

Request example:

```http
GET /GBPRate
Authorization: Bearer <SERVICE_AUTH_KEY>
```

Auth failure response:

```http
401 Unauthorized
The authorization header is missing a Bearer token key or doesn't match the required key.
```

## OpenAPI Contract

`openapi.yaml` defines the API using OpenAPI 3.1.0, including:

- server URL
- endpoint operations
- response formats
- Bearer token security scheme (`type: http`, `scheme: bearer`)

This makes the API easier to integrate with GPT Actions and tooling such as Postman.

## Prerequisites

- Python 3.10+
- Flask and requests
- ExchangeRate-API key: https://v6.exchangerate-api.com
- GPT Actions account if want to demonstrate this: https://chatgpt.com/gpts
- Optional PythonAnywhere account for hosted testing: https://www.pythonanywhere.com

## Local Setup (Windows + VS Code)

```console
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip

pip install pre-commit
pre-commit install
pip install flask requests

$env:EXCHANGE_RATE_API_KEY = "your_exchange_rate_api_key" # pragma: allowlist secret
$env:SERVICE_AUTH_KEY = "your_service_auth_key" # pragma: allowlist secret

$env:FLASK_APP = "plugin.py"
$env:FLASK_ENV = "development"

flask --app plugin run
```

Health check URL:

```text
http://127.0.0.1:5000/
```

## Testing Strategy

### 1) Provider integration test Jupyter notebook

`TestCurrencyAPI.ipynb` calls ExchangeRate-API directly.

Required environment variable:

```console
setx EXCHANGE_RATE_API_KEY "your_exchange_rate_api_key"
```

### 2) Hosted wrapper API test Jupyter notebook

`TestCurrencyPlugin.ipynb` calls the hosted wrapper API on PythonAnywhere (not local Flask).

Required environment variable:

```console
setx SERVICE_AUTH_KEY "your_service_auth_key"
```

If you use `setx`, restart VS Code before running notebook cells.

### 3) API client test

Login to your PythonAnywhere account and upload these 2 files for the "mysite" folder:
- plugin.py and
- openapi.yaml

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

## Ideas for improvements to POC

- Return structured JSON responses with metadata and timestamp.
- Add request timeout/retry handling to upstream provider calls.
- Add automated tests and CI checks.
- Add logging and monitoring for failure visibility.
- Move from single shared token to a stronger auth strategy when scaling.
