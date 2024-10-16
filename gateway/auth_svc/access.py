import os
import requests
from flask import request

def login(request: request):
    auth = request.authorization
    if not auth:
        return None, ("Missing Credentials", 401)

    basicAuth = (auth.username, auth.password)

    response = requests.post(
        f"http://{os.environ.get("AUTH_SVC_ADDRESS")}/login",
        auth=basicAuth
    )

    if response.status_code == 200:
        return response.json(), None

    return None, response.json()
