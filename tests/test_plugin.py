# unittest.mock.Mock lets us replace real function calls with fake ones
# so tests don't make network requests or need real API keys.
import json
from unittest.mock import Mock

# pytest is the test framework. It discovers functions named test_* and runs them automatically.
import pytest

# Import the Flask app module we're testing.
import plugin


# A pytest fixture is a reusable setup helper. When a test function declares `client`
# as a parameter, pytest automatically calls this fixture and passes in the result.
@pytest.fixture
def client():
    # TESTING mode disables Flask's error handling so exceptions surface in tests.
    plugin.app.config["TESTING"] = True
    # test_client() simulates HTTP requests without starting a real server.
    return plugin.app.test_client()


# FakeResponse stands in for the real requests.Response object returned by requests.get().
# The plugin only calls .json() on the response, so that's the only method we need to fake.
class FakeResponse:
    def __init__(self, payload):
        self._payload = payload

    def json(self):
        return self._payload


# -------------------------------------------------------------------
# Each test function follows the Arrange / Act / Assert pattern:
#   Arrange – set up the inputs and environment.
#   Act     – call the code under test.
#   Assert  – verify the outcome matches expectations.
# -------------------------------------------------------------------


def test_health_check_returns_expected_message(client):
    # Act: hit the root endpoint (ie Health Check), which requires no auth and no API key.
    response = client.get("/")

    # Assert: HTTP 200 means the server handled the request successfully.
    assert response.status_code == 200
    # The body must be the exact string the plugin returns for a health check.
    assert (
        response.get_data(as_text=True)
        == "Health Check: Your exchange rate API plugin is working"
    )


def test_gbp_rate_returns_zar_value_when_authenticated(client, monkeypatch):
    # Arrange: monkeypatch temporarily sets environment variables for this test only.
    # They are restored to their original values automatically after the test finishes.
    monkeypatch.setenv("EXCHANGE_RATE_API_KEY", "demo-api-key")
    monkeypatch.setenv("SERVICE_AUTH_KEY", "demo-service-key")

    # Replace requests.get with a Mock that returns our fake provider response.
    # This means no real HTTP call is made to the exchange rate API.
    mock_get = Mock(
        return_value=FakeResponse(
            {
                "conversion_rates": {
                    "ZAR": 23.87,
                }
            }
        )
    )
    # monkeypatch.setattr swaps plugin.requests.get with our mock for this test only.
    monkeypatch.setattr(plugin.requests, "get", mock_get)

    # Act: send a GET request with the correct Bearer token in the Authorization header.
    response = client.get(
        "/GBPRate", headers={"Authorization": "Bearer demo-service-key"}
    )

    # Assert: a successful response returns the ZAR rate as a plain-text number.
    assert response.status_code == 200
    assert response.get_data(as_text=True) == "23.87"
    # Also verify the plugin called the upstream API with the right URL and timeout.
    mock_get.assert_called_once_with(
        f"{plugin.EXCHANGE_RATE_URL}demo-api-key/latest/GBP", timeout=10
    )


def test_usd_rate_returns_zar_value_when_authenticated(client, monkeypatch):
    # Arrange: same pattern as the GBP test, but for the USD endpoint.
    monkeypatch.setenv("EXCHANGE_RATE_API_KEY", "demo-api-key")
    monkeypatch.setenv("SERVICE_AUTH_KEY", "demo-service-key")

    mock_get = Mock(
        return_value=FakeResponse(
            {
                "conversion_rates": {
                    "ZAR": 18.42,
                }
            }
        )
    )
    monkeypatch.setattr(plugin.requests, "get", mock_get)

    # Act
    response = client.get(
        "/USDRate", headers={"Authorization": "Bearer demo-service-key"}
    )

    # Assert
    assert response.status_code == 200
    assert response.get_data(as_text=True) == "18.42"
    mock_get.assert_called_once_with(
        f"{plugin.EXCHANGE_RATE_URL}demo-api-key/latest/USD", timeout=10
    )


@pytest.mark.parametrize(
    "headers",
    [
        {},
        {"Authorization": "Bearer invalid-service-key"},
    ],
)
def test_protected_endpoint_rejects_missing_or_invalid_bearer_token(
    client, monkeypatch, headers
):
    # Arrange: both keys exist, and we exercise both a missing header
    # and an incorrect Bearer token via the parametrized `headers` input.
    monkeypatch.setenv("EXCHANGE_RATE_API_KEY", "demo-api-key")
    monkeypatch.setenv("SERVICE_AUTH_KEY", "demo-service-key")

    # Act: call a protected endpoint without auth or with an invalid token.
    response = client.get("/GBPRate", headers=headers)

    # Assert: the plugin must reject both requests with 401 Unauthorized
    # and return the exact error message defined in plugin.py.
    assert response.status_code == 401
    assert response.get_data(as_text=True) == plugin.ERROR_STRING


def test_protected_endpoint_requires_exchange_rate_api_key(client, monkeypatch):
    # Arrange: simulate the EXCHANGE_RATE_API_KEY not being set in the environment.
    # raising=False means don't raise an error if the variable wasn't already set.
    monkeypatch.delenv("EXCHANGE_RATE_API_KEY", raising=False)
    monkeypatch.setenv("SERVICE_AUTH_KEY", "demo-service-key")

    # Act: the auth header is valid, but the upstream API key is missing.
    response = client.get(
        "/USDRate", headers={"Authorization": "Bearer demo-service-key"}
    )

    # Assert: the plugin must return 500 (server misconfiguration, not a client error)
    # and include the missing-key message so the problem is easy to diagnose.
    assert response.status_code == 500
    assert response.get_data(as_text=True) == plugin.MISSING_KEY_STRING


def test_protected_endpoint_returns_500_when_service_auth_key_is_missing(
    client, monkeypatch
):
    # Arrange: SERVICE_AUTH_KEY is absent — the plugin cannot validate the Bearer token
    # at all, so it raises ValueError before even checking the request header.
    monkeypatch.setenv("EXCHANGE_RATE_API_KEY", "demo-api-key")
    monkeypatch.delenv("SERVICE_AUTH_KEY", raising=False)

    # Act: supply a header that would otherwise be valid; the key check happens first.
    response = client.get(
        "/GBPRate", headers={"Authorization": "Bearer demo-service-key"}
    )

    # Assert: 500 with the specific missing-service-key message (not the API key message).
    assert response.status_code == 500
    assert response.get_data(as_text=True) == plugin.MISSING_SERVICE_KEY_STRING


def test_gbp_rate_returns_504_when_upstream_times_out(client, monkeypatch):
    # Arrange: make requests.get raise Timeout to simulate the provider being slow.
    monkeypatch.setenv("EXCHANGE_RATE_API_KEY", "demo-api-key")
    monkeypatch.setenv("SERVICE_AUTH_KEY", "demo-service-key")

    monkeypatch.setattr(
        plugin.requests, "get", Mock(side_effect=plugin.requests.Timeout)
    )

    # Act
    response = client.get(
        "/GBPRate", headers={"Authorization": "Bearer demo-service-key"}
    )

    # Assert: 504 Gateway Timeout with an informative plain-text message.
    assert response.status_code == 504
    assert "timed out" in response.get_data(as_text=True)


def test_usd_rate_returns_504_when_upstream_times_out(client, monkeypatch):
    # Arrange: same timeout scenario for the USD endpoint.
    monkeypatch.setenv("EXCHANGE_RATE_API_KEY", "demo-api-key")
    monkeypatch.setenv("SERVICE_AUTH_KEY", "demo-service-key")

    monkeypatch.setattr(
        plugin.requests, "get", Mock(side_effect=plugin.requests.Timeout)
    )

    # Act
    response = client.get(
        "/USDRate", headers={"Authorization": "Bearer demo-service-key"}
    )

    # Assert
    assert response.status_code == 504
    assert "timed out" in response.get_data(as_text=True)


def test_gbp_rate_returns_502_when_upstream_request_fails(client, monkeypatch):
    # Arrange: make requests.get raise a generic RequestException (e.g. DNS failure,
    # connection refused) to simulate the provider being unreachable.
    monkeypatch.setenv("EXCHANGE_RATE_API_KEY", "demo-api-key")
    monkeypatch.setenv("SERVICE_AUTH_KEY", "demo-service-key")

    monkeypatch.setattr(
        plugin.requests,
        "get",
        Mock(side_effect=plugin.requests.RequestException("503 Server Error")),
    )

    # Act
    response = client.get(
        "/GBPRate", headers={"Authorization": "Bearer demo-service-key"}
    )

    # Assert: 502 Bad Gateway with a message that includes the underlying error detail.
    assert response.status_code == 502
    assert "Failed to reach the exchange rate API" in response.get_data(as_text=True)


def test_usd_rate_returns_502_when_upstream_request_fails(client, monkeypatch):
    # Arrange: same upstream-failure scenario for the USD endpoint.
    monkeypatch.setenv("EXCHANGE_RATE_API_KEY", "demo-api-key")
    monkeypatch.setenv("SERVICE_AUTH_KEY", "demo-service-key")

    monkeypatch.setattr(
        plugin.requests,
        "get",
        Mock(side_effect=plugin.requests.RequestException("503 Server Error")),
    )

    # Act
    response = client.get(
        "/USDRate", headers={"Authorization": "Bearer demo-service-key"}
    )

    # Assert
    assert response.status_code == 502
    assert "Failed to reach the exchange rate API" in response.get_data(as_text=True)


def test_gbp_rate_returns_502_when_upstream_payload_is_missing_expected_key(
    client, monkeypatch
):
    # Arrange: the provider returns valid JSON but the expected 'conversion_rates' key
    # is absent — simulates an unexpected schema change in the upstream API.
    monkeypatch.setenv("EXCHANGE_RATE_API_KEY", "demo-api-key")
    monkeypatch.setenv("SERVICE_AUTH_KEY", "demo-service-key")

    monkeypatch.setattr(
        plugin.requests,
        "get",
        Mock(
            return_value=FakeResponse({"result": "success"})
        ),  # missing conversion_rates
    )

    # Act
    response = client.get(
        "/GBPRate", headers={"Authorization": "Bearer demo-service-key"}
    )

    # Assert: 502 with a message that names the unexpected-response problem.
    assert response.status_code == 502
    assert "Unexpected response from the exchange rate API" in response.get_data(
        as_text=True
    )


def test_usd_rate_returns_502_when_upstream_response_is_not_valid_json(
    client, monkeypatch
):
    # Arrange: the provider returns a response whose .json() raises JSONDecodeError,
    # simulating an HTML error page or malformed body being returned instead of JSON.
    monkeypatch.setenv("EXCHANGE_RATE_API_KEY", "demo-api-key")
    monkeypatch.setenv("SERVICE_AUTH_KEY", "demo-service-key")

    bad_response = Mock()
    bad_response.json.side_effect = json.JSONDecodeError("Expecting value", "", 0)
    monkeypatch.setattr(plugin.requests, "get", Mock(return_value=bad_response))

    # Act
    response = client.get(
        "/USDRate", headers={"Authorization": "Bearer demo-service-key"}
    )

    # Assert
    assert response.status_code == 502
    assert "Unexpected response from the exchange rate API" in response.get_data(
        as_text=True
    )
