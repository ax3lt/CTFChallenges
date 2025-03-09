import os
import hmac
import hashlib
import base64
import json
from flask import Flask, request, make_response, redirect, render_template

app = Flask(__name__)

USERS = {
    "admin": {"password": "supersecret", "role": "admin"},
}

FLAG = "CTF{HMAC_IS_NOT_ALWAYS_SAFE}"

def get_secret_key(role):
    return f"{role}".encode()

def generate_signed_cookie(username, role):
    payload = {"username": username, "password": USERS[username]["password"], "role": role}
    payload_b64 = base64.b64encode(json.dumps(payload).encode()).decode()

    secret_key = get_secret_key(role)
    signature = hmac.new(secret_key, payload_b64.encode(), hashlib.sha256).hexdigest()

    return payload_b64, signature

def verify_signed_cookie(payload_b64, signature):
    try:
        payload_json = json.loads(base64.b64decode(payload_b64).decode())

        secret_key = get_secret_key(payload_json["role"])
        expected_signature = hmac.new(secret_key, payload_b64.encode(), hashlib.sha256).hexdigest()

        return expected_signature == signature, payload_json
    except Exception:
        return False, None

@app.route("/")
def index():
    username = request.cookies.get("auth_data")
    signature = request.cookies.get("auth_signature")

    if username and signature:
        return redirect("/profile")

    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in USERS:
            return "Questo username è già registrato!"

        USERS[username] = {"password": password, "role": "user"}

        # Genera cookie
        auth_data, auth_signature = generate_signed_cookie(username, "user")
        resp = make_response(redirect("/profile"))
        resp.set_cookie("auth_data", auth_data)
        resp.set_cookie("auth_signature", auth_signature)

        return resp

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = USERS.get(username)
        if user and user["password"] == password:
            auth_data, auth_signature = generate_signed_cookie(username, user["role"])
            resp = make_response(redirect("/profile"))
            resp.set_cookie("auth_data", auth_data)
            resp.set_cookie("auth_signature", auth_signature)
            return resp

        return "Credenziali errate!"

    return render_template("login.html")

@app.route("/profile")
def profile():
    payload_b64 = request.cookies.get("auth_data")
    signature = request.cookies.get("auth_signature")

    if not payload_b64 or not signature:
        return redirect("/login")

    valid, user_data = verify_signed_cookie(payload_b64, signature)

    if not valid:
        return "Cookie non valido!"

    username = user_data["username"]
    role = user_data["role"]
    is_admin = role == "admin"

    return render_template("profile.html", username=username, is_admin=is_admin, flag=FLAG if is_admin else None)

@app.route("/logout")
def logout():
    resp = make_response(redirect("/"))
    resp.set_cookie("auth_data", "", expires=0)
    resp.set_cookie("auth_signature", "", expires=0)
    return resp

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)


