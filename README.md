# Exchange Rate API for GPT Actions

This POC project is a lightweight REST API that exposes two focused currency endpoints for use in a GPT Action:

- GBP to ZAR
- USD to ZAR

It is used to demonstrate a custom GPT Action calling an API for OpenAI GPT Actions and for Dimagi Open Chat Studio Custom Actions (https://github.com/dimagi/open-chat-studio)

## What This Project Demonstrates

- Design: wraps a third-party exchange-rate provider behind an internal API.
- OpenAPI 3.1 specification for GPT Action compatibility. See [OpenAPI](#openapi-contract)
- Security: protected endpoints with HTTP Bearer token. See [Auth Design](#authentication-design)
- Easy deployment: hosted verification path on [PythonAnywhere](./testing/README.md).
- Testing layers: [see here](./testing/README.md)
- Pre-commit hooks: Ruff, Yelp, yaml validation, debug statement checks, security keys
- .env file for keys

## Architecture Overview

1. A Flask web-based API receives client requests.
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

- This is a deliberate security design for testing how GPT Actions and OCS custom actions (as [Authentication Providers](https://docs.openchatstudio.com/concepts/team/authentication_providers/)) handle security
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

This makes the API easier to integrate with GPT Actions, OCS custom actions and tooling such as Postman.

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

pip install python-dotenv

pip install flask requests

$env:EXCHANGE_RATE_API_KEY = "your_exchange_rate_api_key" # pragma: allowlist secret
$env:SERVICE_AUTH_KEY = "your_service_auth_key" # pragma: allowlist secret
```

## Testing Strategy

See [testing notes here](./testing/README.md)


## Ideas for improvements to POC

- Return structured JSON responses with metadata and timestamp.
- Add request timeout/retry handling to upstream provider calls.
- Add logging and monitoring for failure visibility.
- Move from single shared token to a stronger auth strategy when scaling.
