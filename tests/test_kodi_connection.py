import pytest
import requests
import json

# Kodi JSON-RPC endpoint (assuming default setup in CI)
KODI_URL = "http://localhost:8080/jsonrpc"

def send_jsonrpc_request(method, params=None):
    """Helper function to send a JSON-RPC request to Kodi."""
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "id": 1
    }
    if params:
        payload["params"] = params

    response = requests.post(KODI_URL, json=payload, timeout=10)
    response.raise_for_status()  # Raise exception for HTTP errors
    return response.json()

def test_kodi_ping():
    """Test basic connectivity to Kodi server using JSONRPC.Ping."""
    result = send_jsonrpc_request("JSONRPC.Ping")
    assert result.get("result") == "pong", f"Expected 'pong' response, got {result}"

def test_kodi_version():
    """Test retrieving Kodi application version."""
    result = send_jsonrpc_request("Application.GetProperties", {"properties": ["version"]})
    assert "result" in result, f"Expected 'result' in response, got {result}"
    assert "version" in result["result"], f"Expected 'version' in response, got {result['result']}"
    version = result["result"]["version"]
    assert "major" in version, f"Expected 'major' version field, got {version}"
    assert isinstance(version["major"], int), f"Expected integer major version, got {version['major']}"