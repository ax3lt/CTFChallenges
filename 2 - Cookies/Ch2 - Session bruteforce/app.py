import random
from flask import Flask, request, make_response, redirect, render_template

app = Flask(__name__)

USERS = {

}
SESSIONS = {}

FLAG = "CTF{BRUTE_FORCE_MASTER}"

def generate_session_token():
    token = random.randint(0, 50)
    print(f"generated token: {token}")
    return f"session_{token}"

adminToken = generate_session_token()
SESSIONS[adminToken] = "admin"

@app.route("/")
def index():
    token = request.cookies.get("session_token")
    if token and token in SESSIONS:
        return redirect("/profile")
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in USERS:
            return "Questo username è già registrato!"

        USERS[username] = password
        token = generate_session_token()

        while token in SESSIONS:
            token = generate_session_token()

        SESSIONS[token] = username
        resp = make_response(redirect("/profile"))
        resp.set_cookie("session_token", token)
        return resp

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in USERS and USERS[username] == password:
            token = generate_session_token()
            SESSIONS[token] = username
            resp = make_response(redirect("/profile"))
            resp.set_cookie("session_token", token)
            return resp
        else:
            return "Credenziali errate!"

    return render_template("login.html")

@app.route("/profile")
def profile():
    token = request.cookies.get("session_token")
    if not token or token not in SESSIONS:
        return redirect("/login")

    username = SESSIONS[token]
    is_admin = username == "admin"
    return render_template("profile.html", username=username, is_admin=is_admin, flag=FLAG if is_admin else None)

@app.route("/logout")
def logout():
    resp = make_response(redirect("/"))
    resp.set_cookie("session_token", "", expires=0)
    return resp

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
