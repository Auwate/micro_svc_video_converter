import datetime
import os
import jwt
from flask import Flask, request
from flask_mysqldb import MySQL
from MySQLdb.cursors import Cursor

server = Flask(__name__)
mysql = MySQL(server)

server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")

server.route("/login", methods=["POST"])
def login():
    auth = request.authorization

    if not auth:
        return "Missing credentials", 401

    cursor: Cursor = mysql.connection.cursor()

    result = cursor.execute(
        "SELECT email, password" \
        "FROM user" \
        f"WHERE email={auth.username}"
    )

    if result > 0:
        user_row: list = cursor.fetchone()
        email: str = user_row[0]
        password: str = user_row[1]

        if auth.username != email or auth.password != password:
            return "invalid credentials", 401
        else:
            return createJWT(auth.username, os.environ.get("JWT_SECRET"), True)

    else:
        return "Invalid credentials", 401

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
    encoded_jwt = request.headers["Authorization"]

    if not encoded_jwt:
        return "Missing credentials", 401

    encoded_jwt = encoded_jwt.split(" ")

    print(encoded_jwt[0])

    try:
        decoded = jwt.decode(
            encoded_jwt[1],
            os.environ["JWT_SECRET"],
            algorithms=["HS256"]
        )
    except Exception:
        return "Not authorized", 403

    return decoded, 200

if __name__ == "__main__":
    print(__name__)
    server.run(host="0.0.0.0", port=5000)
