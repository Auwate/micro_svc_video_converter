import os

import requests
from flask import request

def token(request: request):
    if "Authorization" not in request.headers:
        return None, {"status": 401, "response": "Missing credentials"}
    token = request.headers["Authorization"]

    if not token:
        return None, {"status": 401, "response": "Missing credentials"}

    response = requests.post(
        f"http://{os.environ.get("AUTH_SVC_ADDRESS")}/validate",
        headers={"Authorization": f"{token}"}
    )

    if response.ok:
        return response.json(), None

    return None, response.json()
