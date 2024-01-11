import requests
import time

def request_authorization(client_id, auth_endpoint, scope):
    """
    Initiates the OAuth2 device flow by requesting authorization.
    """
    data = {
        "client_id": client_id,
        "scope": scope
    }

    response = requests.post(auth_endpoint, data=data)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Authorization request failed with status code {response.status_code}")

def poll_for_token(client_id, device_code, token_endpoint, grant_type):
    """
    Polls the token endpoint for an access token using the device code.
    """
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    token_data = {
        "client_id": client_id,
        "device_code": device_code,
        "grant_type": grant_type
    }

    while True:
        token_response = requests.post(token_endpoint, headers=headers, data=token_data)

        if token_response.status_code == 200:
            return token_response.json()
        elif token_response.status_code != 428:
            raise Exception(f"Token request failed with status code {token_response.status_code}")

        time.sleep(5)  # Poll every 5 seconds
