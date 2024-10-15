import datetime
import os
import jwt
from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.sql import text

server = Flask(__name__)
#master_db = create_engine(f"mysql+pymysql://{os.environ.get("MYSQL_USER")}:{os.environ.get("MYSQL_PASSWORD")}@{os.environ.get("MYSQL_MASTER_DB")}:{os.environ.get("MYSQL_PORT")}/{os.environ.get("MYSQL_DB")}")
replica_db = create_engine(f"mysql+pymysql://{os.environ.get("MYSQL_USER")}:{os.environ.get("MYSQL_PASSWORD")}@{os.environ.get("MYSQL_REPLICA_DB")}:{os.environ.get("MYSQL_PORT")}/{os.environ.get("MYSQL_DB")}")
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

            return {"response": createJWT(email, JWT_SECRET, True)}, 200

        return {"response": "invalid credentials"}, 401

    #cursor: Cursor = mysql.connection.cursor()

    # result = cursor.execute(
    #     "SELECT email, password " \
    #     "FROM user " \
    #     "WHERE email=%s", (auth.username,)
    # )

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
import sys
@server.route("/validate", methods=["POST"])
def validate():

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

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)
