import os
import requests
from flask import request

def token(request: request):
    if "Authorization" not in request.headers:
        return None, ("Missing credentials", 401)
    token = request.headers["Authorization"]

    if not token:
        return None, ("Missing credentials", 401)

    response = requests.post(
        f"http://{os.environ.get("AUTH_SVC_ADDRESS")}/validate"
    )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)
