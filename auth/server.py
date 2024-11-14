import datetime
import os
import jwt
import json
from datetime import timedelta
from redis import Redis
from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.sql import text

server = Flask(__name__)
master_db = create_engine(f"mysql+pymysql://{os.environ.get("MYSQL_USER")}:{os.environ.get("MYSQL_PASSWORD")}@{os.environ.get("MYSQL_MASTER_DB")}:{os.environ.get("MYSQL_PORT")}/{os.environ.get("MYSQL_DB")}")
replica_db = create_engine(f"mysql+pymysql://{os.environ.get("MYSQL_USER")}:{os.environ.get("MYSQL_PASSWORD")}@{os.environ.get("MYSQL_REPLICA_DB")}:{os.environ.get("MYSQL_PORT")}/{os.environ.get("MYSQL_DB")}")
redis_db = Redis(host=f"{os.environ.get("REDIS_HOST")}", port=f"{int(os.environ.get("REDIS_PORT"))}")
JWT_SECRET = os.environ.get("JWT_SECRET")

# server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
# server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
# server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
# server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
# server.config["MYSQL_PORT"] = int(os.environ.get("MYSQL_PORT"))

# mysql = MySQL(server)

@server.route("/login", methods=["POST"])
def login():
    auth = request.authorization

    if not auth:
        return {"response": "missing credentials"}, 401

    with replica_db.connect() as connection:

        command = text(
            "SELECT email, password "
            "FROM user "
            "WHERE email=:param1"
        )

        result = connection.execute(
            command,
            {"param1": auth.username}
        )

        row = result.fetchone()

        if row:
            email: str = row[0]
            password: str = row[1]

            if email != auth.username or password != auth.password:
                return {"response": "invalid credentials"}, 401

            updateAccessed(email)

            return {"response": createJWT(email, JWT_SECRET, True)}, 200

        return {"response": "invalid credentials"}, 401

    #cursor: Cursor = mysql.connection.cursor()

    # result = cursor.execute(
    #     "SELECT email, password " \
    #     "FROM user " \
    #     "WHERE email=%s", (auth.username,)
    # )

def updateAccessed(email: str):

    with master_db.connect() as connection:

        command = text(
            "UPDATE user "
            "SET accessed = NOW() "
            "WHERE email=:param1"
        )

        connection.execute(
            command,
            {"param1": email}
        )

        connection.commit()

def createJWT(username: str, secret: str, isAdmin: bool):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc)
            + datetime.timedelta(days=1),
            "iat": datetime.datetime.now(datetime.timezone.utc),
            "admin": isAdmin
        },
        secret,
        algorithm="HS256",
    )

@server.route("/validate", methods=["POST"])
def validate():

    if not request.headers or "Authorization" in request.headers:
        return {"response": "missing credentials"}, 401

    encoded_jwt = request.headers["Authorization"]

    if not encoded_jwt:
        return {"response": "missing credentials"}, 401

    encoded_jwt = encoded_jwt.split(" ")

    try:
        decoded = jwt.decode(
            encoded_jwt[1],
            os.environ["JWT_SECRET"],
            algorithms=["HS256"]
        )
    except Exception:
        return {"response": "not authorized"}, 403

    return {"response": decoded}, 200

@server.route("/admin/recent", methods=["GET"])
def mostRecentlyAccessed():
    """
    Admin API

    Returns the accounts that have recently accessed the API
    """
    if not request.headers or "Authorization" not in request.headers:
        return {"response": "missing credentials"}, 401

    encoded_jwt = request.headers["Authorization"]

    if not encoded_jwt:
        return {"response": "missing credentials"}, 401

    encoded_jwt = encoded_jwt.split(" ")

    try:
        decoded_jwt = jwt.decode(
            encoded_jwt[1],
            os.environ["JWT_SECRET"],
            algorithms=["HS256"]
        )

        if not decoded_jwt.get("admin"):
            return {"response": "not authorized"}, 403

    except Exception:
        return {"response": "not authorized"}, 403

    # Try Redis

    recentlyAccessedData = redis_db.get("recentlyAccessed")

    if recentlyAccessedData:
        return {"response": json.loads(recentlyAccessedData)}, 200

    # Else fill Redis and then return

    with replica_db.connect() as connection:

        sql_query = text(
            "SELECT email, DATE_FORMAT(accessed, '%m/%d/%Y %H:%i:%s') AS formatted_access "
            "FROM user "
            "ORDER BY accessed DESC"
        )

        result = connection.execute(sql_query)

        rows = result.fetchall()

        response = [{"email": row[0], "accessed": row[1]} for row in rows]

        redis_db.set("recentlyAccessed", json.dumps(response), ex=timedelta(hours=1))

        return {"response": response}, 200

    return {"response": "server error"}, 500

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)
